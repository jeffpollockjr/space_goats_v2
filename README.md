# Space Goats v2 — AI Simulation

A terminal-based Python simulation of **Space Goats v2**, a strategic card game where AI-controlled players battle for dominance through rockets, shields, and grass-based colony building.

## Overview

All gameplay is fully automated with AI players making strategic decisions each turn. Watch as goat-piloted spaceships defend their hulls, fire rockets into orbit zones, and race to accumulate enough space grass to win by colony. No human input required.

**Game Features:**
- 2-5 AI-controlled players
- Fully deterministic game loop with configurable randomization
- Complex card stack system for action resolution
- Two victory conditions: Combat Victory (last ship standing) or Colony Victory (grass accumulation)
- Terminal-based logging of every turn, phase, and action
- 104 unique cards with 14 different booster passive effects

## Quick Start

### Requirements
- Python 3.7+
- No external libraries (uses only Python standard library)

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/space_goats_v2.git
cd space_goats_v2
```

### Running a Game

```bash
python3 main.py
```

The simulation will run a complete game and output a detailed log to the terminal showing every action, decision, and game state change.

## Configuration

Edit `main.py` to customize the game:

```python
# Number of players (2-5)
NUM_PLAYERS = 5

# Print detailed game log (True/False)
VERBOSE_LOG = True

# Random seed for reproducible games (None = random)
RANDOM_SEED = None
```

### Colony Victory Threshold

Scales automatically with player count:
- 2 players: 10 Grass cards
- 3 players: 12 Grass cards
- 4 players: 14 Grass cards
- 5 players: 16 Grass cards

## Game Overview

### The Setup
Each player receives one unique ship and a starting hand of 5 cards drawn from the Shared Pile. Ships are identical in mechanics (4 upgrade slots, 1 Hull HP) but differ in name for identity.

### Turn Structure (5 Phases)

1. **Phase 1 — Draw**
   - Draw 1 card from Shared Pile
   - Discard pile shuffles into Shared Pile if empty

2. **Phase 2 — Orbit Resolution**
   - AI decides which rockets in Orbit Zone fire or hold
   - Each fired rocket opens a Card Stack window for opponent responses

3. **Phase 3 — Resource**
   - Draw 1 Space Grass card into personal stockpile
   - Check if Colony Victory threshold reached
   - Opponents may play Steal cards in response

4. **Phase 4 — Play**
   - Play Shields and Boosters to ship slots
   - Stage rockets to Orbit Zone (max 2, modified by boosters)
   - Fire Laser Rockets immediately
   - Use Grass Spend ability (trade 2 Grass for 1 card draw)

5. **Phase 5 — End**
   - Discard down to 5-card hand limit

### Card Types

**Rockets (25 cards)**
- Standard Rockets (19): Stage to Orbit Zone, fire in Phase 2
- Laser Rockets (6): Fire immediately when played

**Shields (19 cards)**
- Attach to ship slots, absorb 1 rocket hit, then destroyed
- Only Shields protect the Hull

**Boosters (14 cards)**
- Passive effects while attached (draw bonuses, orbit cap increase, etc.)
- Never destroyed by rockets (only Sabotage special cards)
- Can be discarded to make room for new boosters

**Special Cards (23 cards)**
- **Intercept (5)**: Destroy or redirect a declared rocket
- **Steal (5)**: Take 1 Grass from opponent's stockpile
- **Sabotage (5)**: Destroy opponent's Shield or Booster
- **Repair (4)**: Recover Shield or Booster from discard pile
- **Launch (4)**: Instantly stage a rocket to Orbit Zone

**Space Grass (18 cards)**
- Collected in Phase 3 (never drawn to hand)
- Path to Colony Victory
- Can be spent in Phase 4 (2 cards = 1 card draw)

### The Card Stack

When a rocket fires or special card is played:
1. Event placed on stack
2. All players get chance to respond with Special Cards
3. New responses open new windows (recursive)
4. Once all pass, stack resolves top-to-bottom
5. Events that are no longer valid "fizzle" harmlessly

**Key Rules:**
- Rockets only target Shields, hitting Hull if none remain
- Rockets targets declared at firing time, not when staged
- Steal can only remove obstacles to Colony Victory if target has Grass
- Intercept destroys rockets before they hit
- Repair restores cards from discard pile

## Project Structure

```
space_goats_v2/
├── main.py              # Entry point — configure and run game
├── game.py              # Game loop and win condition checks
├── state.py             # Data structures (Card, Ship, Player, GameState)
├── deck.py              # All 104 cards and pile construction
├── cards.py             # Card effect logic and booster mechanics
├── stack.py             # Card Stack resolution system
├── turns.py             # 5-phase turn engine implementation
├── ai.py                # AI player decision making
├── logger.py            # Terminal output and game logging
├── .gitignore           # Git exclusion rules
└── README.md            # This file
```

## AI Strategy

AI players use sensible heuristics:

- **Rocket Firing**: Fire if opponent has no shields (direct hull hit), or if orbit zone at cap
- **Card Playing**: Shields first, then boosters, then rockets
- **Responding**: Play Intercept if targeted with no shields, Steal if opponent wins
- **Grass Spend**: Only if hand depleted and far from colony victory

AI never makes illegal moves and prioritizes survival over aggression.

## Example Game Session

```
================================================================================
SPACE GOATS — v2 AI SIMULATION
A terminal-based strategic card game
================================================================================

Game Starting:
  Players: 3
  Starting Hand: 5 cards each
  Colony Victory Threshold: 12

================================================================================
TURN 1 — Player 1 (The Baaad Omen)
================================================================================

[PHASE 1 - DRAW] Player 1
  → Draws: Billy's Bad Idea

[PHASE 3 - RESOURCE] Player 1
  → Draws 1 Space Grass
    Stockpile: 1/12 Grass

[PHASE 4 - PLAY] Player 1
  → Plays: The Tin Fleece (Shield) into Slot 1

[PHASE 5 - END] Player 1

--- GAME STATE ---
Player 1     ● [THE - - -] O:0/2 G:1
Player 2     ● [- - - -] O:0/2 G:0
Player 3     ● [- - - -] O:0/2 G:0

Shared Pile: 76 | Grass Pile: 17 | Discard: 0

... game continues ...

GAME OVER — Player 2 WINS!
  Victory Condition: Combat Victory
  Game lasted 22 turns
```

## Victory Conditions

**Combat Victory** — Last player with undestroyed ship wins
**Colony Victory** — Accumulate enough Space Grass equal to player threshold

## Booster Effects

The 14 unique boosters provide passive bonuses:

| Booster | Effect |
|---------|--------|
| The Extra Nibble | +1 card on Draw Phase |
| Orbit Expander 3000 | +1 to Orbit Zone cap |
| The Discount Grazer | Grass Spend costs 1 instead of 2 |
| The Nosy Snout | Peek top of Shared Pile once/turn |
| The Freeloader | Draw 1 when any player uses Grass Spend |
| Grief Wool | Draw 1 when your Shield destroyed |
| The Generous Gate | Draw 1 when you attach Shield |
| The Panic Button | Once per game, fire rocket outside Phase 2 |
| The Overgrown Engine | +1 Grass on Resource Phase |
| The Barbed Fence | Steal requires 2+ Special Cards on stack |
| Double Dip Drive | Grass Spend draws 2 cards instead of 1 |
| The Periscope Horn | Peek opponent's hand once/turn |
| The Silver Lining | Draw 1 when your rocket intercepted |
| The Revolving Hoof | Discarded slot cards return to hand |

## Troubleshooting

**Game runs very long?**
- This is normal. Games with more players (5) can exceed 50+ turns
- Modify `RANDOM_SEED` in main.py for different outcomes

**Not seeing all players in game state?**
- Terminal window may need to be wider
- Try maximizing terminal or reducing verbosity

**All players eliminated?**
- Game will end when only 1 player remains (Combat Victory)
- Check the final game result message

## Development Notes

- Written in pure Python 3 (no external dependencies)
- Uses Python standard library: `random`, `dataclasses`, `enum`, `typing`
- Fully deterministic with optional seeding
- Designed for easy rule additions and card expansions

## License

This project is a fan implementation for educational purposes. Space Goats is a strategic card game.

## Contributing

Feel free to submit issues, feature requests, or improvements! Possible enhancements:
- Additional AI strategies
- Game statistics tracking
- Network multiplayer support
- Interactive human player mode
- Additional booster effects and cards

---

**Enjoy watching the goats battle it out!** 🐐🚀
