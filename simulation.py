#!/usr/bin/env python3
"""
Space Goats v2 — Multi-Game Simulation and Statistics

Run multiple games of Space Goats v2 and collect comprehensive statistics
on win rates, victory types, game lengths, and player performance.

Usage:
    python3 simulation.py
    
Configure the constants below to adjust simulation parameters.
"""

from collections import defaultdict
from game import SpaceGoatsGame
import time


# ============================================================================
# Configuration
# ============================================================================

NUM_SIMULATIONS = 500
NUM_PLAYERS = 5
SHOW_PROGRESS = True  # Print progress every N games
PROGRESS_INTERVAL = 50


# ============================================================================
# Simulation Runner
# ============================================================================

def run_simulations(num_sims: int, num_players: int, show_progress: bool = True) -> dict:
    """
    Run multiple games and collect statistics.
    
    Returns:
        Dictionary with comprehensive game statistics
    """
    
    # Statistics containers
    wins_by_player = defaultdict(int)
    wins_by_player_and_condition = defaultdict(lambda: defaultdict(int))
    victory_types = defaultdict(int)
    game_lengths = []
    
    print(f"\n{'='*80}")
    print(f"RUNNING {num_sims} SIMULATIONS WITH {num_players} PLAYERS")
    print(f"{'='*80}\n")
    
    start_time = time.time()
    
    for sim_num in range(1, num_sims + 1):
        # Run a single game
        game = SpaceGoatsGame(
            num_players=num_players,
            verbose=False,  # Silent mode for speed
            random_seed=None
        )
        
        winner, win_condition = game.run_game()
        
        # Collect statistics
        wins_by_player[winner.name] += 1
        wins_by_player_and_condition[winner.name][win_condition] += 1
        victory_types[win_condition] += 1
        game_lengths.append(game.game_state.turn_count)
        
        # Progress indicator
        if show_progress and (sim_num % PROGRESS_INTERVAL == 0 or sim_num == 1):
            elapsed = time.time() - start_time
            rate = sim_num / elapsed
            remaining = (num_sims - sim_num) / rate if rate > 0 else 0
            print(f"  Progress: {sim_num:3d}/{num_sims} games | "
                  f"Elapsed: {elapsed:6.1f}s | ETA: {remaining:6.1f}s")
    
    elapsed_total = time.time() - start_time
    
    # Compile results
    results = {
        'num_sims': num_sims,
        'num_players': num_players,
        'wins_by_player': dict(wins_by_player),
        'wins_by_condition': dict(wins_by_player_and_condition),
        'victory_types': dict(victory_types),
        'game_lengths': game_lengths,
        'elapsed_time': elapsed_total,
    }
    
    return results


# ============================================================================
# Statistics Reporting
# ============================================================================

def print_statistics(results: dict) -> None:
    """Print comprehensive statistics from simulation results."""
    
    num_sims = results['num_sims']
    num_players = results['num_players']
    wins_by_player = results['wins_by_player']
    wins_by_condition = results['wins_by_condition']
    victory_types = results['victory_types']
    game_lengths = results['game_lengths']
    elapsed = results['elapsed_time']
    
    print(f"\n{'='*80}")
    print(f"SIMULATION RESULTS")
    print(f"{'='*80}\n")
    
    # Overall stats
    print(f"Games Simulated: {num_sims}")
    print(f"Players per Game: {num_players}")
    print(f"Total Time: {elapsed:.2f} seconds")
    print(f"Average Time per Game: {(elapsed / num_sims):.3f} seconds\n")
    
    # Win rates by player
    print("─" * 80)
    print("WIN RATES BY PLAYER")
    print("─" * 80)
    
    sorted_players = sorted(wins_by_player.items(), key=lambda x: x[1], reverse=True)
    for player_name, wins in sorted_players:
        win_pct = (wins / num_sims) * 100
        win_bar = "█" * int(win_pct / 2) + "░" * (50 - int(win_pct / 2))
        print(f"{player_name:16} {wins:4d} wins ({win_pct:5.1f}%) {win_bar}")
    
    # Victory type distribution
    print(f"\n{'─' * 80}")
    print("VICTORY TYPE DISTRIBUTION")
    print("─" * 80)
    
    sorted_victories = sorted(victory_types.items(), key=lambda x: x[1], reverse=True)
    for vtype, count in sorted_victories:
        vtype_pct = (count / num_sims) * 100
        v_bar = "█" * int(vtype_pct / 2) + "░" * (50 - int(vtype_pct / 2))
        print(f"{vtype:25} {count:4d} wins ({vtype_pct:5.1f}%) {v_bar}")
    
    # Victory breakdown by player
    print(f"\n{'─' * 80}")
    print("VICTORY BREAKDOWN BY PLAYER")
    print("─" * 80)
    
    for player_name in sorted(wins_by_player.keys()):
        conditions = wins_by_condition.get(player_name, {})
        combat_wins = conditions.get('Combat Victory', 0)
        colony_wins = conditions.get('Colony Victory', 0)
        other_wins = conditions.get('Game Limit Exceeded', 0)
        total = combat_wins + colony_wins + other_wins
        
        print(f"\n{player_name}:")
        if combat_wins > 0:
            print(f"  Combat Victory: {combat_wins:4d} ({(combat_wins/total)*100:5.1f}% of their wins)")
        if colony_wins > 0:
            print(f"  Colony Victory: {colony_wins:4d} ({(colony_wins/total)*100:5.1f}% of their wins)")
        if other_wins > 0:
            print(f"  Other:          {other_wins:4d} ({(other_wins/total)*100:5.1f}% of their wins)")
    
    # Game length statistics
    print(f"\n{'─' * 80}")
    print("GAME LENGTH STATISTICS (in turns)")
    print("─" * 80)
    
    avg_length = sum(game_lengths) / len(game_lengths)
    min_length = min(game_lengths)
    max_length = max(game_lengths)
    median_length = sorted(game_lengths)[len(game_lengths) // 2]
    
    # Calculate quartiles
    sorted_lengths = sorted(game_lengths)
    q1 = sorted_lengths[len(sorted_lengths) // 4]
    q3 = sorted_lengths[3 * len(sorted_lengths) // 4]
    
    print(f"Average:          {avg_length:6.1f} turns")
    print(f"Median:           {median_length:6} turns")
    print(f"Min:              {min_length:6} turns")
    print(f"Max:              {max_length:6} turns")
    print(f"Q1 (25th %ile):   {q1:6} turns")
    print(f"Q3 (75th %ile):   {q3:6} turns")
    print(f"Std Dev:          {calculate_std_dev(game_lengths):6.1f} turns")
    
    # Distribution histogram
    print(f"\nGame Length Distribution (by 5-turn buckets):")
    buckets = defaultdict(int)
    for length in game_lengths:
        bucket = (length // 5) * 5
        buckets[bucket] += 1
    
    for bucket in sorted(buckets.keys()):
        count = buckets[bucket]
        pct = (count / num_sims) * 100
        bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
        print(f"  {bucket:3d}-{bucket+4:3d} turns: {count:4d} games ({pct:5.1f}%) {bar}")
    
    # Balance analysis
    print(f"\n{'─' * 80}")
    print("GAME BALANCE ANALYSIS")
    print("─" * 80)
    
    win_pcts = [(player, (wins / num_sims) * 100) for player, wins in wins_by_player.items()]
    avg_win_pct = sum(pct for _, pct in win_pcts) / len(win_pcts)
    max_deviation = max(abs(pct - avg_win_pct) for _, pct in win_pcts)
    
    print(f"Expected win rate per player: {avg_win_pct:.2f}%")
    print(f"Max deviation from average:   {max_deviation:.2f}%")
    
    if max_deviation < 5:
        balance = "EXCELLENT - Very balanced"
    elif max_deviation < 10:
        balance = "GOOD - Reasonably balanced"
    elif max_deviation < 15:
        balance = "FAIR - Some balance issues"
    else:
        balance = "POOR - Significant imbalance"
    
    print(f"Balance Assessment:           {balance}")
    
    # Footer
    print(f"\n{'='*80}\n")


def calculate_std_dev(values: list) -> float:
    """Calculate standard deviation."""
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance ** 0.5


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    try:
        # Run simulations
        results = run_simulations(
            num_sims=NUM_SIMULATIONS,
            num_players=NUM_PLAYERS,
            show_progress=SHOW_PROGRESS
        )
        
        # Print results
        print_statistics(results)
        
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
    except Exception as e:
        print(f"\nError during simulation: {e}")
        import traceback
        traceback.print_exc()
