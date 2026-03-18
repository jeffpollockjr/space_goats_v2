"""
Space Goats v2 — AI Player Logic

Simple but sensible AI that plays legal moves without being unbeatable.
AI players make decisions for every phase and stack response.
"""

import random
from typing import List, Optional, Tuple

from state import GameState, Player, Card, CardType, SpecialSubtype
from cards import (
    has_booster,
    get_orbit_zone_cap,
    get_grass_spend_cost,
)
from turns import (
    play_shield_to_slot,
    play_booster_to_slot,
    stage_rocket_to_orbit,
    fire_laser_rocket,
    grass_spend,
    peek_shared_pile,
    peek_opponent_hand,
)


class AIPlayer:
    """
    Represents an AI-controlled player.
    
    Handles all decisions: which rockets to fire, which cards to play,
    which special cards to respond with, whether to spend Grass.
    """
    
    def __init__(self, player: Player):
        self.player = player
        self.has_peeked_shared_pile_this_turn = False
        self.has_peeked_opponent_hand_this_turn = False
    
    # ========================================================================
    # Phase 2 — Fire or Hold Each Rocket
    # ========================================================================
    
    def decide_phase_2_fire(self, player: Player, game_state: GameState) -> None:
        """
        Decide which rockets to fire in Phase 2.
        
        Decision rules:
        - Fire if target has no Shields (direct Hull hit)
        - Fire if Orbit Zone at cap and want to stage new rocket in Phase 4
        - Hold if just detected threat (opponent Shield plays)
        - Otherwise fire if held for 2+ turns (simplified: fire if any rockets)
        """
        from stack import StackEvent
        
        # Make a copy of orbit_zone to iterate safely
        rockets_in_orbit = player.ship.orbit_zone.copy()
        
        for rocket in rockets_in_orbit:
            # Choose a target (for now, random opponent)
            targets = game_state.get_other_players(exclude_eliminated=True)
            if not targets:
                continue
            
            target = random.choice(targets)
            
            # Decide whether to fire this rocket
            should_fire = self._should_fire_rocket(player, rocket, target, game_state)
            
            if should_fire:
                # Remove from Orbit Zone
                player.ship.orbit_zone.remove(rocket)
                
                # Create a stack event for the rocket firing
                event = StackEvent(
                    trigger_type="rocket_fired",
                    source_player=player,
                    target_player=target,
                    card=rocket
                )
                
                # Push to stack
                game_state.card_stack.push(event)
                
                # Open response window (will be handled in game loop)
    
    def _should_fire_rocket(self, player: Player, rocket: Card, 
                           target: Player, game_state: GameState) -> bool:
        """Determine if a rocket should be fired."""
        # Always fire if target has no shields (direct Hull hit)
        if target.ship.get_shield_count() == 0:
            return True
        
        # Fire if at Orbit Zone cap (to make room for staging)
        cap = get_orbit_zone_cap(player)
        if len(player.ship.orbit_zone) >= cap:
            return True
        
        # Hold otherwise (conservative strategy)
        return False
    
    # ========================================================================
    # Phase 4 — Play Cards
    # ========================================================================
    
    def decide_phase_4_play(self, player: Player, game_state: GameState) -> None:
        """
        Decide which cards to play in Phase 4.
        
        Play order: Shields → Boosters → Rockets → Laser Rockets → Special/Grass
        
        The AI plays cards that are beneficial this turn, respecting slot limits
        and Orbit Zone cap.
        """
        self.has_peeked_shared_pile_this_turn = False
        self.has_peeked_opponent_hand_this_turn = False
        
        # Play Shields first (defensive priority)
        self._play_shields(player, game_state)
        
        # Play Boosters if slots open
        self._play_boosters(player, game_state)
        
        # Stage a rocket if Orbit Zone not at cap
        self._stage_rocket(player, game_state)
        
        # Fire Laser Rockets if opponent vulnerable
        self._fire_laser_rockets(player, game_state)
        
        # Consider Grass Spend if hand is depleted
        self._consider_grass_spend(player, game_state)
        
        # Play Special Cards reactively (happens during opponent turns mainly)
    
    def _play_shields(self, player: Player, game_state: GameState) -> None:
        """Play Shield cards to open slots."""
        shields = [c for c in player.hand if c.card_type == CardType.SHIELD]
        
        for shield in shields:
            # Find first open slot
            for i, slot in enumerate(player.ship.slots):
                if slot is None:
                    play_shield_to_slot(player, shield, i, game_state)
                    break
    
    def _play_boosters(self, player: Player, game_state: GameState) -> None:
        """Play Booster cards to slots."""
        boosters = [c for c in player.hand if c.card_type == CardType.BOOSTER]
        
        for booster in boosters:
            # Find first open slot
            for i, slot in enumerate(player.ship.slots):
                if slot is None:
                    play_booster_to_slot(player, booster, i, game_state)
                    break
            
            # If no open slot, consider replacing a weaker booster
            # (simplified: don't replace for now)
    
    def _stage_rocket(self, player: Player, game_state: GameState) -> None:
        """Stage a Standard Rocket to Orbit Zone."""
        rockets = [c for c in player.hand if c.card_type == CardType.STANDARD_ROCKET]
        
        if rockets:
            rocket = rockets[0]
            cap = get_orbit_zone_cap(player)
            if len(player.ship.orbit_zone) < cap:
                stage_rocket_to_orbit(player, rocket, game_state)
    
    def _fire_laser_rockets(self, player: Player, 
                           game_state: GameState) -> None:
        """Fire Laser Rockets at vulnerable opponents."""
        # Laser rockets cannot be played until after the first round
        if game_state.turn_count <= 1:
            return
        
        laser_rockets = [c for c in player.hand if c.card_type == CardType.LASER_ROCKET]
        
        for laser in laser_rockets:
            # Find opponent with no shields
            targets = game_state.get_other_players(exclude_eliminated=True)
            for target in targets:
                if target.ship.get_shield_count() == 0:
                    fire_laser_rocket(player, laser, target, game_state)
                    # After firing, we need to handle stack resolution
                    # This is handled in the game loop
                    break
    
    def _consider_grass_spend(self, player: Player, 
                             game_state: GameState) -> None:
        """Consider spending Grass for extra cards."""
        # Only spend if hand is nearly empty and Grass stockpile is healthy
        if len(player.grass_stockpile) < 2:
            return  # Not enough Grass
        
        cost = get_grass_spend_cost(player)
        if len(player.grass_stockpile) < cost:
            return  # Can't afford
        
        # Don't spend if close to Colony Victory
        threshold = self._get_colony_victory_threshold(game_state)
        if len(player.grass_stockpile) >= threshold - 2:
            return  # Too close to victory
        
        # Spend if hand is nearly empty
        if len(player.hand) <= 2:
            grass_spend(player, game_state)
    
    # ========================================================================
    # Stack Response — Special Cards
    # ========================================================================
    
    def decide_stack_response(self, event, game_state: GameState) -> Optional[Card]:
        """
        Decide whether to respond to a stack event with a Special Card.
        
        Returns a Special Card from hand if responding, None otherwise.
        """
        # Handle Colony Victory events (card is None)
        if event.card is None:
            return self._respond_to_colony_victory(event, game_state)
        
        # Handle rocket firing
        if event.card.card_type != CardType.SPECIAL:
            return self._respond_to_rocket(event, game_state)
        
        # Could implement further response logic for other special cards
        return None
    
    def _respond_to_rocket(self, event, game_state: GameState) -> Optional[Card]:
        """Decide whether to respond to a rocket firing."""
        # If this AI is the target and at risk, play Intercept
        if event.target_player == self.player:
            intercepts = [c for c in self.player.hand 
                         if c.card_type == CardType.SPECIAL 
                         and c.subtype == SpecialSubtype.INTERCEPT]
            
            if intercepts and self.player.ship.get_shield_count() == 0:
                # No shields, play Intercept to save ship
                return intercepts[0]
        
        return None
    
    def _respond_to_colony_victory(self, event, game_state: GameState) -> Optional[Card]:
        """Decide whether to respond to a Colony Victory declaration."""
        # Only respond if the declaring player is not us
        if event.source_player == self.player:
            return None
        
        # Try to play Steal to block the victory
        steals = [c for c in self.player.hand 
                 if c.card_type == CardType.SPECIAL 
                 and c.subtype == SpecialSubtype.STEAL]
        
        if steals and len(event.source_player.grass_stockpile) > 0:
            # Play a Steal card against the declaring player
            return steals[0]
        
        return None
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def _get_colony_victory_threshold(self, game_state: GameState) -> int:
        """Get the Grass threshold for this player count."""
        # Colony victory threshold is 6 cards for all player counts
        return 6
    
    def get_best_target_for_rocket(self, player: Player, 
                                   game_state: GameState) -> Optional[Player]:
        """Choose the best target for a rocket attack."""
        candidates = game_state.get_other_players(exclude_eliminated=True)
        
        if not candidates:
            return None
        
        # Prefer targets with no shields (direct hull hit)
        for candidate in candidates:
            if candidate.ship.get_shield_count() == 0:
                return candidate
        
        # Otherwise attack opponent with fewest shields
        candidates.sort(key=lambda p: p.ship.get_shield_count())
        return candidates[0]
    
    def select_discard_for_hand_limit(self, player: Player) -> Card:
        """Select a card to discard when over hand limit."""
        # Discard special cards least urgently needed first
        special_cards = [c for c in player.hand if c.card_type == CardType.SPECIAL]
        if special_cards:
            return special_cards[0]
        
        # Otherwise discard first card
        return player.hand[0]
