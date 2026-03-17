#!/usr/bin/env python3
"""
Space Goats v2 — AI Simulation Entry Point

Run the Space Goats v2 card game simulation with AI-controlled players.
All gameplay is simulated automatically with no human interaction.

Usage:
    python main.py

Configuration:
    Modify the constants below to customize game parameters.
"""

from game import SpaceGoatsGame


# ============================================================================
# Configuration Constants
# ============================================================================

# Number of players (2-5 supported)
NUM_PLAYERS = 5

# Whether to print detailed game log
VERBOSE_LOG = True

# Whether to pause between turns (press Enter to continue)
PAUSE_BETWEEN_TURNS = False

# Random seed for reproducible games (None for random seed)
RANDOM_SEED = None

# Maximum turns before game is forced to end (safety limit)
MAX_TURNS = 1000


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Run a complete Space Goats v2 game simulation."""
    
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print(f"Error: NUM_PLAYERS must be 2-5, got {NUM_PLAYERS}")
        return
    
    # Create and run game
    game = SpaceGoatsGame(
        num_players=NUM_PLAYERS,
        verbose=VERBOSE_LOG,
        random_seed=RANDOM_SEED
    )
    
    # Run the game to completion
    winner, win_condition = game.run_game()
    
    # Print final result
    if winner:
        print(f"\n\n{'='*80}")
        print(f"FINAL RESULT")
        print(f"{'='*80}")
        print(f"Winner: {winner.name} ({winner.ship.name})")
        print(f"Victory Condition: {win_condition}")
        print(f"Final Grass Stockpile: {len(winner.grass_stockpile)} cards")
        print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
