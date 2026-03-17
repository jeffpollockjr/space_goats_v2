"""
Space Goats v2 — Terminal Output and Game Logger

Formats and prints clear, readable game state and action log.
"""

from typing import List
from state import GameState, Player, CardType


class GameLogger:
    """Handles all terminal output and logging."""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.log_buffer = []
    
    def log(self, message: str) -> None:
        """Add a message to the log buffer."""
        if self.verbose:
            print(message)
            self.log_buffer.append(message)
    
    def print_section_divider(self) -> None:
        """Print a major section divider."""
        self.log("=" * 80)
    
    def print_minor_divider(self) -> None:
        """Print a minor section divider."""
        self.log("-" * 80)
    
    # ========================================================================
    # Turn and Phase Announcements
    # ========================================================================
    
    def announce_turn_start(self, game_state: GameState) -> None:
        """Announce the start of a player's turn."""
        self.print_section_divider()
        player = game_state.get_current_player()
        self.log(f"TURN {game_state.turn_count} — {player.name} ({player.ship.name})")
        self.print_section_divider()
    
    def announce_phase(self, phase: int, player_name: str) -> None:
        """Announce the current phase."""
        phase_names = {
            1: "DRAW",
            2: "ORBIT RESOLUTION",
            3: "RESOURCE",
            4: "PLAY",
            5: "END",
        }
        name = phase_names.get(phase, "UNKNOWN")
        self.log(f"\n[PHASE {phase} - {name}] {player_name}")
    
    # ========================================================================
    # Phase Actions
    # ========================================================================
    
    def log_draw(self, player: Player, cards_drawn: List) -> None:
        """Log cards drawn in Phase 1."""
        if cards_drawn:
            card_str = ", ".join(c.name for c in cards_drawn)
            self.log(f"  → Draws: {card_str}")
    
    def log_orbit_resolution(self, player: Player, rockets_fired: List,
                            rockets_held: List) -> None:
        """Log rockets fired/held in Phase 2."""
        if rockets_fired:
            for rocket, target in rockets_fired:
                self.log(f"  → Fires: {rocket.name} at {target.name}")
                self.log(f"    (Stack window open for responses...)")
        
        if rockets_held:
            self.log(f"  → Holds: {len(rockets_held)} rocket(s) in Orbit Zone")
    
    def log_resource(self, player: Player, grass_collected: List) -> None:
        """Log Grass collected in Phase 3."""
        total_grass = len(player.grass_stockpile)
        self.log(f"  → Draws {len(grass_collected)} Space Grass")
        self.log(f"    Stockpile: {total_grass}/{self._get_colony_threshold(None)} Grass")
    
    def log_play(self, player: Player, action: str) -> None:
        """Log a card played in Phase 4."""
        self.log(f"  → {action}")
    
    def log_end(self, player: Player, discards: List) -> None:
        """Log Phase 5 end of turn."""
        if discards:
            card_str = ", ".join(c.name for c in discards)
            self.log(f"  → Discards down to 5: {card_str}")
    
    # ========================================================================
    # Game State Display
    # ========================================================================
    
    def print_game_state(self, game_state: GameState) -> None:
        """Print a detailed snapshot of all players' current state."""
        self.print_minor_divider()
        self.log("--- GAME STATE ---")
        
        for player in game_state.get_active_players():
            self.print_player_state(player, game_state)
        
        self.log("")
        self.log(f"Shared Pile: {len(game_state.shared_pile)} | "
                f"Grass Pile: {len(game_state.grass_pile)} | "
                f"Discard: {len(game_state.discard_pile)}")
    
    def print_player_state(self, player: Player, game_state: GameState) -> None:
        """Print a single player's ship and resource state."""
        ship = player.ship
        
        # Hull status
        hull_status = "●" if ship.hull_hp > 0 else "✗"
        
        # Slots status - more compact
        slot_strs = []
        for slot in ship.slots:
            if slot is None:
                slot_strs.append("-")
            else:
                # Truncate to 3 chars for compactness
                name = slot.name[:3].upper()
                slot_strs.append(name)
        slots_str = " ".join(slot_strs)
        
        # Orbit Zone status
        orbit = len(ship.orbit_zone)
        cap = self._get_orbit_cap(player)
        
        # Grass count
        grass = len(player.grass_stockpile)
        
        self.log(f"{player.name:12} {hull_status} [{slots_str}] O:{orbit}/{cap} G:{grass}")
    
    # ========================================================================
    # Stack Resolution
    # ========================================================================
    
    def announce_stack_window_open(self) -> None:
        """Announce that a stack window has opened for responses."""
        self.log("  → Stack window open for responses...")
    
    def log_stack_response(self, responding_player: Player, response_card) -> None:
        """Log a player responding to a stack event."""
        self.log(f"    {responding_player.name} plays: {response_card.name}")
    
    def log_stack_all_pass(self) -> None:
        """Log that all players passed on the stack window."""
        self.log("    → All players pass. Stack resolves...")
    
    def log_stack_resolution_step(self, message: str) -> None:
        """Log a step in stack resolution."""
        self.log(f"    {message}")
    
    # ========================================================================
    # Win Conditions
    # ========================================================================
    
    def announce_colony_victory_check(self, player: Player, 
                                     threshold: int) -> None:
        """Announce a Colony Victory check."""
        grass_count = len(player.grass_stockpile)
        self.log(f"\n  [COLONY VICTORY CHECK]")
        self.log(f"  {player.name} has {grass_count} Grass (threshold: {threshold})")
        
        if grass_count >= threshold:
            self.log(f"  → COLONY VICTORY DECLARED! (Stack window open for Steal responses...)")
    
    def announce_colony_victory_confirmed(self, player: Player) -> None:
        """Announce that Colony Victory has been confirmed."""
        self.log(f"\n  ★ {player.name} wins by COLONY VICTORY! ★")
    
    def announce_combat_victory(self, winner: Player, loser: Player) -> None:
        """Announce that a player has been eliminated."""
        self.log(f"\n  ★ {loser.name}'s ship destroyed! ★")
        self.log(f"  {loser.name} is eliminated.")
    
    def announce_game_over(self, winner: Player, win_condition: str,
                          turn_count: int) -> None:
        """Announce the end of the game."""
        self.print_section_divider()
        self.log(f"\n  GAME OVER — {winner.name} WINS!")
        self.log(f"  Victory Condition: {win_condition}")
        self.log(f"  Game lasted {turn_count} turns")
        self.log(f"  Ship: {winner.ship.name}\n")
        self.print_section_divider()
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def _get_colony_threshold(self, game_state) -> int:
        """Get the Colony Victory threshold (simplified placeholder)."""
        # This would normally come from game_state
        return 12
    
    def _get_orbit_cap(self, player: Player) -> int:
        """Get this player's Orbit Zone cap."""
        from cards import get_orbit_zone_cap
        return get_orbit_zone_cap(player)
    
    def print_welcome(self) -> None:
        """Print welcome message."""
        self.print_section_divider()
        self.log("SPACE GOATS — v2 AI SIMULATION")
        self.log("A terminal-based strategic card game")
        self.print_section_divider()
    
    def print_game_setup(self, game_state: GameState) -> None:
        """Print game setup information."""
        self.log(f"\nGame Starting:")
        self.log(f"  Players: {len(game_state.players)}")
        self.log(f"  Starting Hand: 5 cards each")
        self.log(f"  Colony Victory Threshold: {self._get_colony_threshold(game_state)}")
        self.print_minor_divider()
