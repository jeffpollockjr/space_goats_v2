# Space Goats v2 — AI Simulation Build Instructions

---

## Overview

You are building a **terminal-based Python simulation** of Space Goats v2 — a 2–5 player strategic card game. The game is played entirely by AI players. There is no human input. The simulation runs from the terminal and prints a clear, readable log of every action, decision, and game state change so the game can be followed turn by turn.

All game rules, card types, and card effects are defined in two companion files:
- `space_goats_v2_spec.md` — full game rules, turn structure, and mechanics
- `space_goats_v2_cards.md` — all 104 cards with names and effects

**Read both files in full before writing any code.**

---

## Tech Stack

- **Language:** Python 3
- **No external libraries required** — use only Python standard library (random, dataclasses, enum, typing, copy)
- **Entry point:** `main.py`
- **Run command:** `python main.py`
- **Player count:** Default to 3 AI players. Make player count configurable at the top of `main.py` as a constant.

---

## Project Structure

```
space_goats/
├── main.py              # Entry point — configure player count, run game
├── game.py              # Core game loop and win condition checks
├── state.py             # All data structures (GameState, Player, Ship, OrbitZone)
├── deck.py              # Deck and pile construction, shuffling, drawing
├── turns.py             # Turn engine — 5 phases in strict order
├── cards.py             # Card definitions, types, and effect logic
├── stack.py             # Card Stack system — trigger windows, resolution
├── ai.py                # AI player decision making
└── logger.py            # Terminal output formatting and game log
```

---

## Build Order

Build and verify each step before moving to the next. Do not skip ahead.

### Step 1 — Data Structures (`state.py`)
Build all game state objects first. Everything else depends on these.

```python
# Key objects to define:
- Card(name, card_type, subtype, effect)
- Ship(name, hull_hp=1, slots=[], orbit_zone=[])
- Player(name, ship, hand=[], grass_stockpile=[])
- GameState(players, shared_pile, grass_pile, discard_pile, card_stack, current_player_index)
```

**Rules to encode:**
- Ship has exactly 4 slots
- Orbit Zone cap is 2 rockets per ship
- Hand limit is 5 cards
- Hull HP is 1
- Grass stockpile is a list of physical cards, not a number

---

### Step 2 — Deck & Pile Construction (`deck.py`)

Build the two piles separately from the card definitions in `space_goats_v2_cards.md`.

**Shared Pile (81 cards):**
- 19 Standard Rockets
- 6 Laser Rockets
- 19 Shields
- 14 Boosters
- 5 Special — Intercept
- 5 Special — Steal
- 5 Special — Sabotage
- 4 Special — Repair
- 4 Special — Launch

**Grass Pile (18 cards):**
- 18 Space Grass cards

**Ship Cards (5 cards):**
- Dealt directly to players at setup — never shuffled into either pile

**Setup sequence:**
1. Create all 5 ship cards and deal one to each player
2. Build and shuffle the Grass Pile
3. Build and shuffle the Shared Pile
4. Deal 5 cards from the Shared Pile to each player's hand

---

### Step 3 — Turn Engine (`turns.py`)

Implement the 5 phases in strict order. Each phase must be a separate function.

```python
def phase_1_draw(player, game_state)
def phase_2_orbit_resolution(player, game_state)
def phase_3_resource(player, game_state)
def phase_4_play(player, game_state)
def phase_5_end(player, game_state)
```

**Critical rules per phase:**

**Phase 1 — Draw:**
- Draw 1 card from Shared Pile into hand
- If Shared Pile empty, shuffle discard pile to form new Shared Pile

**Phase 2 — Orbit Resolution:**
- AI chooses to fire or hold each rocket (see AI section)
- Firing a rocket opens a Card Stack window before it resolves
- Rocket targets are declared at firing — not when staged
- Fired rockets hit one Shield of attacker's choice, or Hull if no Shields remain
- Boosters are never valid rocket targets
- Held rockets stay in Orbit Zone

**Phase 3 — Resource:**
- Draw 1 card from Grass Pile into player's grass stockpile
- If Grass Pile empty, skip this phase entirely
- After collecting, check Colony Victory condition

**Phase 4 — Play:**
- AI plays cards in this order: Shields first, then Boosters, then Rockets, then Laser Rockets
- Stage max 1 Standard Rocket per turn into Orbit Zone
- Cannot exceed Orbit Zone cap of 2 — must fire before staging if at cap
- Laser Rockets fire immediately and open a Card Stack window
- Grass Spend: return 2 Grass cards to bottom of Grass Pile, draw 1 from Shared Pile
- Special Cards are open timing — AI may play them here or in response to other events

**Phase 5 — End:**
- Discard down to hand limit of 5 cards
- Pass turn to next player clockwise

---

### Step 4 — Card Effects (`cards.py`)

Define card types as enums and implement effect logic for each.

```python
class CardType(Enum):
    STANDARD_ROCKET = "standard_rocket"
    LASER_ROCKET = "laser_rocket"
    SHIELD = "shield"
    BOOSTER = "booster"
    SPACE_GRASS = "space_grass"
    SPECIAL = "special"

class SpecialSubtype(Enum):
    INTERCEPT = "intercept"
    STEAL = "steal"
    SABOTAGE = "sabotage"
    REPAIR = "repair"
    LAUNCH = "launch"
```

**Implement each effect as a function:**

```python
def effect_intercept(rocket, game_state)       # Destroy or redirect a declared rocket
def effect_steal(target_player, game_state)    # Take 1 Grass from target stockpile
def effect_sabotage(target_player, slot_index, game_state)  # Destroy Shield or Booster in slot
def effect_repair(player, card_to_recover, game_state)      # Recover card from discard to slot
def effect_launch(player, rocket_card, game_state)          # Stage rocket instantly to Orbit Zone
```

**Booster passive effects — implement each individually:**

| Booster Name | Effect to implement |
|---|---|
| The Extra Nibble | +1 card on Draw Phase |
| Orbit Expander 3000 | Orbit Zone cap +1 |
| The Discount Grazer | Grass Spend costs 1 instead of 2 |
| The Nosy Snout | AI peeks top of Shared Pile once per turn |
| The Freeloader | Draw 1 when any player uses Grass Spend |
| Grief Wool | Draw 1 when owner's Shield is destroyed |
| The Generous Gate | Draw 1 when owner attaches a Shield |
| The Panic Button | Once per game, fire rocket outside Phase 2 — then discard this card |
| The Overgrown Engine | +1 Grass on Resource Phase |
| The Barbed Fence | Steal cards require 2+ Special Cards on stack to target this player's Grass |
| Double Dip Drive | Grass Spend draws 2 cards instead of 1 |
| The Periscope Horn | AI peeks one opponent's hand once per turn |
| The Silver Lining | Draw 1 when owner's rocket is intercepted |
| The Revolving Hoof | Discarded slot cards return to hand instead of discard pile |

---

### Step 5 — Card Stack (`stack.py`)

This is the most complex system. Build it carefully.

```python
class StackEvent:
    trigger_type  # "rocket_fired" or "special_card_played"
    source_player
    target_player
    card          # the card or rocket involved

class CardStack:
    events = []   # list of StackEvent objects, bottom to top
    
    def push(event)
    def resolve()       # resolve top to bottom
    def is_empty()
    def open_window()   # ask all AI players if they want to respond
```

**Resolution rules:**
1. A rocket is declared firing OR a Special Card is played → push to stack
2. Open response window — iterate through all other players in turn order
3. Each AI player decides whether to play a Special Card in response (see AI section)
4. Once all players pass, resolve stack top to bottom
5. Before each event resolves, check if it is still valid — if not, it fizzles
6. Discard resolved cards

**Fizzle conditions:**
- Intercept targets a rocket that was already destroyed by a card above it → fizzle
- Steal targets a player with 0 Grass → fizzle
- Sabotage targets a slot that is now empty → fizzle
- Repair targets a card no longer in the discard pile → fizzle

---

### Step 6 — AI Player Logic (`ai.py`)

AI players make decisions for every phase. Keep AI logic simple but sensible — it should play a legal, reasonable game without being unbeatable.

```python
class AIPlayer:
    def decide_phase_2(self, game_state)   # fire or hold each rocket
    def decide_phase_4(self, game_state)   # which cards to play and in what order
    def decide_stack_response(self, stack_event, game_state)  # whether to respond
    def decide_grass_spend(self, game_state)   # whether to spend grass for a card
```

**AI decision guidelines:**

*Phase 2 — Fire or Hold:*
- Fire if target opponent has no Shields (direct Hull hit — always fire)
- Fire if Orbit Zone is at cap and AI wants to stage a new rocket in Phase 4
- Hold if target opponent just played a Shield and AI suspects an Intercept card
- Otherwise fire if rockets have been held for 2+ turns

*Phase 4 — Playing Cards:*
- Always play Shields if slots are open and hand has Shields
- Play Boosters if slots are open and no Shields needed urgently
- Stage a rocket if Orbit Zone is not at cap
- Play Laser Rocket if an opponent's Hull is exposed (no Shields)
- Use Grass Spend if hand is empty and Grass stockpile has 3+ cards
- Never spend Grass if within 2 cards of Colony Victory threshold

*Stack Response — Special Cards:*
- Play Intercept if a rocket is targeting this AI and it has no Shields
- Play Steal if an opponent declares Colony Victory
- Play Sabotage if an opponent attaches a Booster that is particularly threatening
- Play Repair if a Shield was just destroyed and a slot is open
- Play Launch if AI has a rocket in hand and wants to apply surprise pressure

*General AI rules:*
- AI never makes illegal moves
- AI prioritizes survival over winning — it will shield up before attacking
- AI pursues Colony Victory quietly if it accumulates 6+ Grass without being targeted

---

### Step 7 — Terminal Output (`logger.py`)

Print clear, readable game state at each phase. Use dividers and labels so the log is easy to follow.

```
========================================
TURN 3 — The Cud Bucket
========================================
[PHASE 1 - DRAW] The Cud Bucket draws: Billy's Bad Idea (Standard Rocket)

[PHASE 2 - ORBIT RESOLUTION] The Cud Bucket has 1 rocket in Orbit Zone.
  → Fires: Udder Devastation at The Grazing Fury
  → Stack window open...
  → The Grazing Fury plays: Wool Over Your Eyes (Intercept) — rocket destroyed!
  → Stack resolves. Rocket fizzled.

[PHASE 3 - RESOURCE] The Cud Bucket draws 1 Space Grass. Stockpile: 4
  → Grass Pile remaining: 11 cards

[PHASE 4 - PLAY]
  → Plays: The Tin Fleece (Shield) into Slot 2
  → Stages: Hoof-Seeking Missile into Orbit Zone [Orbit Zone: 1/2]

[PHASE 5 - END] The Cud Bucket discards down to 5 cards.

--- GAME STATE ---
The Baaad Omen    | Hull: INTACT | Slots: [Wool Wall] [Hoof Plate Alpha] [--] [--] | Orbit: 0/2 | Grass: 2
The Grazing Fury  | Hull: INTACT | Slots: [Barnyard Barrier] [--] [--] [--] | Orbit: 1/2 | Grass: 3
The Cud Bucket    | Hull: INTACT | Slots: [Tin Fleece] [--] [--] [--] | Orbit: 1/2 | Grass: 4
-----------------
Shared Pile: 44 cards | Grass Pile: 11 cards | Discard: 18 cards
========================================
```

---

### Step 8 — Win Condition Checks (`game.py`)

Check win conditions at the correct moments:

**Colony Victory:**
- Check immediately after Phase 3 Resource collection
- If stockpile meets or exceeds threshold, open a Card Stack window for Steal responses
- If stack resolves and stockpile still meets threshold → Colony Victory confirmed
- Thresholds: 2 players = 10, 3 players = 12, 4 players = 14, 5 players = 16

**Combat Victory:**
- Check after every rocket resolves
- If a Hull is hit, that player is eliminated
- Return their Grass stockpile cards to the bottom of the Grass Pile
- Discard their hand and attached ship cards
- If only 1 player remains → Combat Victory

**Game end:**
- Print winner, winning condition, and final game state
- Print a brief summary of how many turns the game lasted

---

## Important Rules to Get Right

These are the most commonly misimplemented rules — pay special attention:

1. **Rockets only target Shields** — never Boosters. If no Shields, rocket hits Hull directly.
2. **Orbit Zone targets are declared at firing** — not when staged. A rocket in the Orbit Zone has no target until Phase 2.
3. **Firing is optional in Phase 2** — AI may hold rockets. But if at cap (2), must fire before staging in Phase 4.
4. **Slot replacement costs the current card** — discarding it to hand is not allowed. Goes to discard pile.
5. **Grass cards never enter a player's hand** — they go directly to the face-up stockpile from the Grass Pile.
6. **Grass Spend returns cards to the bottom of the Grass Pile** — not the discard pile.
7. **Eliminated player's Grass goes to bottom of Grass Pile** — not the discard pile.
8. **Card Stack opens on two triggers** — rocket declared firing, OR Special Card played.
9. **Laser Rockets open a stack window** — opponents may respond before it hits.
10. **The Barbed Fence Booster** — Steal cards can only target this player's Grass if 2+ Special Cards are already on the stack.

---

## Configuration Constants (top of `main.py`)

```python
NUM_PLAYERS = 3          # 2–5 players
VERBOSE_LOG = True       # Print full game log
PAUSE_BETWEEN_TURNS = False  # Set True to pause and press Enter each turn
RANDOM_SEED = None       # Set an integer for reproducible games
```

---

## Final Checklist Before Running

- [ ] All 81 Shared Pile cards are present and correctly typed
- [ ] All 18 Grass Pile cards are present
- [ ] All 5 Ship cards deal correctly at setup
- [ ] Turn order is strictly Phase 1 → 2 → 3 → 4 → 5
- [ ] Card Stack resolves top to bottom
- [ ] Fizzle conditions are checked before each stack event resolves
- [ ] Colony Victory threshold scales with player count
- [ ] Eliminated player Grass returns to Grass Pile
- [ ] No card effect causes an illegal game state

---

*Build Document Version: 1.0 — Python terminal simulation of Space Goats v2. Reference space_goats_v2_spec.md (v3.4) and space_goats_v2_cards.md (v2.1) for all rules and card definitions.*
