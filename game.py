"""
Space Goats v2 — Game Loop and Win Conditions

Manages the overall game flow, turn sequence, win condition checks,
and game initialization.
"""

from typing import Optional, Tuple

from state import GameState, Player, Ship, Card, CardType
from deck import create_game_piles
from ai import AIPlayer
from logger import GameLogger
from turns import (
    phase_1_draw,
    phase_2_orbit_resolution,
    phase_3_resource,
    phase_4_play,
    phase_5_end,
)
from stack import CardStack, resolve_stack, StackEvent


class SpaceGoatsGame:
    """Main game controller for Space Goats v2."""
    
    def __init__(self, num_players: int = 5, verbose: bool = True, 
                 random_seed: int = None):
        """
        Initialize the game.
        
        Args:
            num_players: Number of players (2-5)
            verbose: Whether to print detailed log
            random_seed: Random seed for reproducibility
        """
        self.num_players = num_players
        self.verbose = verbose
        self.logger = GameLogger(verbose)
        self.game_state = None
        self.ai_players = []
        self.random_seed = random_seed
        self.winner = None
        self.win_condition = None
    
    # ========================================================================
    # Setup and Initialization
    # ========================================================================
    
    def setup_game(self) -> None:
        """Initialize the game state and deal cards."""
        self.logger.print_welcome()
        
        # Create piles
        shared_pile, grass_pile, ship_cards = create_game_piles(self.random_seed, self.num_players)
        
        # Prepare starting shields for 2-player duels
        starting_shields = []
        if self.num_players == 2:
            from deck import SHIELDS
            # Use the first 2 shields as starting equipment (not from the pile)
            starting_shields = [SHIELDS[0], SHIELDS[1]]
        
        # Create players
        ship_names = [card.name for card in ship_cards]
        players = []
        
        for i in range(self.num_players):
            ship = Ship(name=ship_names[i])
            player = Player(name=f"Player {i + 1}", ship=ship)
            
            # For 2-player duels, attach a starting shield to slot 0
            if self.num_players == 2 and i < len(starting_shields):
                player.ship.slots[0] = starting_shields[i]
            
            players.append(player)
        
        # Create game state
        self.game_state = GameState(
            players=players,
            shared_pile=shared_pile,
            grass_pile=grass_pile,
            card_stack=CardStack()
        )
        
        # Deal 5 cards to each player
        for _ in range(5):
            for player in players:
                if self.game_state.shared_pile:
                    card = self.game_state.shared_pile.pop(0)
                    player.hand.append(card)
        
        # Create AI players
        self.ai_players = [AIPlayer(p) for p in players]
        
        # Log setup
        self.logger.print_game_setup(self.game_state)
    
    # ========================================================================
    # Main Game Loop
    # ========================================================================
    
    def run_game(self) -> Tuple[Player, str]:
        """
        Run the game to completion.
        
        Returns:
            (winner, win_condition) — the winning player and how they won
        """
        self.setup_game()
        
        max_turns = 1000  # Safety limit
        turn = 0
        
        while turn < max_turns:
            turn += 1
            self.game_state.turn_count = turn
            
            # Check if only one player remains (Combat Victory condition)
            active = self.game_state.get_active_players()
            if len(active) == 1:
                self.winner = active[0]
                self.win_condition = "Combat Victory"
                self.logger.announce_game_over(self.winner, self.win_condition, turn)
                return self.winner, self.win_condition
            
            # Take turns for each player
            for player_index in range(self.num_players):
                # Skip eliminated players
                if self.game_state.players[player_index].is_eliminated:
                    continue
                
                self.game_state.current_player_index = player_index
                player = self.game_state.get_current_player()
                ai = self.ai_players[player_index]
                
                # Execute turn
                self.execute_turn(player, ai)
                
                # Check for winner after each turn
                active = self.game_state.get_active_players()
                if len(active) == 1:
                    self.winner = active[0]
                    self.win_condition = "Combat Victory"
                    self.logger.announce_game_over(self.winner, self.win_condition, turn)
                    return self.winner, self.win_condition
                
                # Check if the current player just won by Colony Victory
                # (set during execute_turn)
                if self.winner is not None:
                    return self.winner, self.win_condition
        
        # Safety: No winner after max turns
        active = self.game_state.get_active_players()
        if active:
            self.winner = active[0]
            self.win_condition = "Game Limit Exceeded"
            return self.winner, self.win_condition
    
    # ========================================================================
    # Turn Execution
    # ========================================================================
    
    def execute_turn(self, player: Player, ai: AIPlayer) -> None:
        """Execute one complete turn for a player."""
        self.logger.announce_turn_start(self.game_state)
        
        # Phase 1 — Draw
        self.logger.announce_phase(1, player.name)
        phase_1_draw(player, self.game_state)
        self.logger.log_draw(player, player.hand[-1:])
        
        # Phase 2 — Orbit Resolution
        if len(player.ship.orbit_zone) > 0:
            self.logger.announce_phase(2, player.name)
            phase_2_orbit_resolution(player, self.game_state, ai)
            self._resolve_all_stacks()
            self._cleanup_eliminations()
        
        # Phase 3 — Resource / Grass Collection
        self.logger.announce_phase(3, player.name)
        grass_collected = player.grass_stockpile.copy()
        should_check_colony = phase_3_resource(player, self.game_state)
        
        if should_check_colony:
            threshold = self._get_colony_threshold()
            self.logger.announce_colony_victory_check(player, threshold)
            
            # Open stack window for Steal responses
            if len(player.grass_stockpile) >= threshold:
                self._handle_colony_victory_stack_window(player, threshold)
                
                # Check if still meets threshold after Steals
                if len(player.grass_stockpile) >= threshold:
                    self.winner = player
                    self.win_condition = "Colony Victory"
                    self.logger.announce_colony_victory_confirmed(player)
        else:
            self.logger.log_resource(player, grass_collected)
        
        # Phase 4 — Play
        self.logger.announce_phase(4, player.name)
        phase_4_play(player, self.game_state, ai)
        self._resolve_all_stacks()
        self._cleanup_eliminations()
        
        # Phase 5 — End
        self.logger.announce_phase(5, player.name)
        phase_5_end(player, self.game_state)
        
        # Print updated game state
        self.logger.print_game_state(self.game_state)
    
    # ========================================================================
    # Stack Resolution During Game
    # ========================================================================
    
    def _resolve_all_stacks(self) -> None:
        """Resolve all pending stack events."""
        while not self.game_state.card_stack.is_empty():
            event = self.game_state.card_stack.events[0]
            
            # Try to get responses from other players
            self._ask_for_responses(event)
            
            # Resolve the stack
            resolve_stack(self.game_state, self.logger.log_stack_resolution_step)
    
    def _ask_for_responses(self, event: StackEvent) -> None:
        """Ask all players if they want to respond to a stack event."""
        self.logger.announce_stack_window_open()
        
        # Ask each other player in turn order if they want to respond
        source_index = self.game_state.players.index(event.source_player)
        
        for offset in range(1, self.num_players):
            player_index = (source_index + offset) % self.num_players
            player = self.game_state.players[player_index]
            
            if player.is_eliminated:
                continue
            
            ai = self.ai_players[player_index]
            response_card = ai.decide_stack_response(event, self.game_state)
            
            if response_card:
                self.logger.log_stack_response(player, response_card)
                player.hand.remove(response_card)
                
                # Add response to stack
                response_event = StackEvent(
                    trigger_type="special_card_played",
                    source_player=player,
                    target_player=event.target_player,
                    card=response_card
                )
                self.game_state.card_stack.push(response_event)
                
                # Recursively ask for more responses
                self._ask_for_responses(response_event)
                return
        
        self.logger.log_stack_all_pass()

    # ========================================================================
    # Elimination Cleanup
    # ========================================================================

    def _cleanup_eliminations(self) -> None:
        """
        Explicitly clean up any newly eliminated players after stack resolution.

        When a ship is destroyed in cards.py, the attacker already receives
        the victim's Grass stockpile directly. This method acts as a safety net
        — if any eliminated player still has Grass on their object for any
        reason, it is sent to the Grass Pile rather than silently orphaned.
        It also handles the standard cleanup of the eliminated player's hand
        and attached ship cards.
        """
        for player in self.game_state.players:
            if not player.is_eliminated:
                continue

            # Safety net: if any Grass remains on the eliminated player
            # (should be empty after cards.py transfer, but guard against
            # edge cases such as simultaneous eliminations), return it
            # to the bottom of the Grass Pile.
            if player.grass_stockpile:
                self.game_state.grass_pile.extend(player.grass_stockpile)
                player.grass_stockpile.clear()

            # Discard the eliminated player's hand
            if player.hand:
                self.game_state.discard_pile.extend(player.hand)
                player.hand.clear()

            # Discard all cards attached to the eliminated player's ship slots
            for i, slot in enumerate(player.ship.slots):
                if slot is not None:
                    self.game_state.discard_pile.append(slot)
                    player.ship.slots[i] = None

            # Clear the orbit zone (rockets in transit are discarded)
            if player.ship.orbit_zone:
                self.game_state.discard_pile.extend(player.ship.orbit_zone)
                player.ship.orbit_zone.clear()

    # ========================================================================
    # Win Conditions
    # ========================================================================
    
    def _get_colony_threshold(self) -> int:
        """Get the Colony Victory Grass threshold for current player count."""
        # Colony victory threshold is 12 cards for all player counts
        return 12
    
    def _handle_colony_victory_stack_window(self, declaring_player: Player,
                                           threshold: int) -> None:
        """
        Handle stack window for Steal responses to Colony Victory.
        
        Opponents may play Steal cards to reduce the declaring player's
        Grass stockpile before Colony Victory is confirmed.
        """
        # Create a fake event for the Colony Victory
        event = StackEvent(
            trigger_type="colony_victory",
            source_player=declaring_player,
            target_player=declaring_player,
            card=None
        )
        
        self._ask_for_responses(event)
        
        # Resolve any Steal cards that were played
        resolve_stack(self.game_state, self.logger.log_stack_resolution_step)
    
    # ========================================================================
    # Utility
    # ========================================================================
    
    def get_game_result(self) -> Tuple[Optional[Player], Optional[str]]:
        """Get the game result (winner and condition)."""
        return self.winner, self.win_condition