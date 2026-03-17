# Space Goats — v2 Game Design Specification

---

## Overview

**Space Goats** is a 2–5 player strategic card game combining combat, resource management, and precision timing. Players pilot asymmetric ships, build defenses with shields and upgrades, fire rockets into a shared Orbit Zone, and race to either destroy all opponent ships or secretly stockpile enough Space Grass to win by colony.

---

## Players & Setup

| Players | Space Grass Win Threshold |
|---------|--------------------------|
| 2       | 10 Grass                 |
| 3       | 12 Grass                 |
| 4       | 14 Grass                 |
| 5       | 16 Grass                 |

### Setup Steps
1. Separate all 5 **Ship Cards** from the deck and deal one to each player face-up in front of them.
2. Separate all 18 **Space Grass Cards** from the deck and shuffle them into their own face-down **Grass Pile**. Place it in a visible shared area.
3. Shuffle the remaining 81 cards into the face-down **Shared Pile**. Place it next to the Grass Pile.
4. Each player draws **5 cards** from the Shared Pile as their starting hand.
5. Determine a starting player (e.g. most recent space-related movie watched goes first).
6. Each player places their Ship Card in their **play area**. Space Grass is tracked physically — drawn Grass cards are kept face-up in front of each player as their personal stockpile.

---

## Win Conditions

There are two ways to win:

1. **Combat Victory** — You are the last player with an undestroyed ship.
2. **Colony Victory** — The physical Grass cards in your personal stockpile equal or exceed the threshold for your player count at the end of your Resource Phase.

The Colony Victory is intentionally difficult to pull off — opponents can target your grass stockpile with Special Cards. A successful colony win is a strategic achievement.

---

## The Ship

Each player controls one **Ship Card**. Ships are the same structurally but each has a unique **passive perk** (see Ship Archetypes below).

### Ship Stats (All Ships)
- **Hull HP:** 1 — if the Hull is hit, the ship is destroyed
- **Upgrade Slots:** 4 — cards can be attached here (shields, boosters)
- **Destruction Rule:** The Hull can only be hit by a Rocket or Laser that reaches it directly. **Only Shields protect the Hull** — Boosters do not block incoming rockets. The Hull is exposed the moment no Shields remain, regardless of how many Boosters are attached.

### Shield & Slot Rules
- Shields and Boosters occupy one slot each.
- A ship may have a maximum of 4 attached cards at any time.
- Incoming Rockets **only target Shields** — they cannot target Boosters. If the target ship has no Shields but has Boosters in slots, the rocket bypasses the Boosters and hits the Hull directly.
- Shields have **1 HP** — one hit destroys them and they are discarded.
- Boosters are **never** destroyed by rocket hits. They can only be removed by Sabotage Special Cards.
- **Slot Replacement:** You may play a new card into any **open** slot freely. To replace an **occupied** slot, you must first **discard the card currently in it** — it cannot be returned to your hand. Only then may you attach the new card. Choose carefully — discarded slot cards are gone.
- A player whose ship is destroyed is eliminated. Their hand and any attached ship cards are discarded. Their face-up Grass stockpile cards are returned to the **bottom of the Grass Pile**.

---

## Ship Archetypes

All ships are identical in stats and abilities — 4 slots, 1 Hull HP, no unique perks. The five ships differ in name only, giving players a sense of identity without mechanical asymmetry.

| Ship Name | Archetype |
|-----------|-----------|
| **The Baaad Omen** | Combat |
| **The Grazing Fury** | Combat |
| **The Cud Bucket** | Defense |
| **The Bleating Heart** | Utility |
| **The Herd Ship Mentality** | Resource |

---

## Turn Structure

Each player takes a full turn in clockwise order. A turn has **5 phases**, resolved in strict order:

### Phase 1 — Draw
Draw **1 card** from the **Shared Pile** into your hand.
- If the Shared Pile is empty, shuffle its discard pile to form a new Shared Pile.

### Phase 2 — Orbit Resolution
For each rocket currently in **your personal Orbit Zone**, you **choose** whether to fire it or hold it:
- **Fire:** Choose a target ship. The rocket hits one Shield of your choice. If no Shields remain, it hits the Hull — destroying the ship. Fired rockets are discarded.
- **Hold:** The rocket stays in your Orbit Zone and carries over to your next Orbit Resolution phase. You may continue adding rockets to the Orbit Zone up to your cap.

> **Orbit Zone Cap:** Default ships hold a maximum of **2 rockets**. If you are already at your cap, you must fire at least one rocket before you can stage a new one in Phase 4.
> If you have no rockets in your Orbit Zone, skip this phase.

### Phase 3 — Resource
Draw **1 card** from the **Grass Pile** and place it face-up in your personal stockpile.
- If the Grass Pile is empty, skip this phase entirely — no Grass is collected that turn.
- After collecting, count your stockpile. If it meets or exceeds the win threshold, **immediately declare Colony Victory** and win the game.
- Opponents may play **Steal-type Special Cards** in response before the win is confirmed.

### Phase 4 — Play
Play any number of cards from your hand in any order. Card types that can be played this phase:

- **Rockets** → Stage **1 rocket** into your Orbit Zone per turn. Cannot exceed your Orbit Zone cap of 2 — must fire at least one before staging if at cap.
- **Laser Rockets** → Bypass the Orbit Zone entirely — hit a target **immediately**.
- **Shields** → Attach to one of your open ship slots.
- **Boosters** → Attach to one of your open ship slots.
- **Grass Spend** → Return 2 Grass cards from your personal stockpile to the **bottom of the Grass Pile**, then draw 1 card from the **Shared Pile**.

> Laser Rockets do not count toward the Orbit Zone cap — they fire immediately.
> **Special Cards may be played at any time** — on your turn or any opponent's turn. See the Special Cards section for full details.

### Phase 5 — End
Discard down to **5 cards** (hand limit). Your turn ends. Play passes clockwise.

---

## Card Types

### Rockets (Standard)
- Stage **1 rocket per turn** into your personal Orbit Zone during Phase 4 (Gunship may stage 2).
- Firing is **optional** each Orbit Resolution phase — you may hold rockets in the Orbit Zone to build up pressure.
- Default Orbit Zone cap: **2 rockets**. If at cap, must fire at least one before staging a new one.
- Upon firing, choose a target ship. The rocket hits one Shield of your choice. If no Shields remain, it hits the Hull — destroying the ship. Boosters are never a valid rocket target.

### Laser Rockets (Bypass)
- Fire **immediately** when played — skip the Orbit Zone entirely.
- Otherwise follow the same targeting rules as standard rockets.
- Rarer than standard rockets — fewer copies in the deck.

### Shields
- Attach to an open ship slot during Phase 4.
- Absorb 1 incoming rocket hit, then are destroyed.
- If a Shield is hit, it is removed from the slot — the slot becomes open again.

### Boosters
- Attach to an open ship slot during Phase 4.
- Provide a passive effect while attached (see card list).
- NOT destroyed by rocket hits unless a Special Card specifically targets them.
- Example booster effects: draw an extra card, reduce incoming laser damage, hold an extra rocket in orbit.

### Space Grass Cards
- Space Grass cards live in their own dedicated **Grass Pile** — separate from the Shared Pile.
- They are **never drawn into a player's hand**. They are only collected during Phase 3.
- Collected Grass cards are kept **face-up in front of each player** as their physical stockpile. The card count is your stockpile total.
- **Spend Ability:** During Phase 4, return 2 Grass cards from your stockpile to the **bottom of the Grass Pile** to draw 1 card from the Shared Pile. This is a deliberate tradeoff — spending Grass moves you further from Colony Victory and replenishes the Grass Pile for other players.
- Some Special Cards can steal Grass cards directly from an opponent's stockpile.

### Special Cards
Special Cards are **open timing** — they may be played at any point during the game, on your turn or on any opponent's turn. They can be used proactively to press an advantage or reactively to counter an opponent's action. A player may hold Special Cards in hand and deploy them the moment the situation calls for it.

Four Special Card subtypes exist, each with a natural moment of use:

| Subtype | Natural Trigger | Description |
|---------|----------------|-------------|
| **Intercept** | When a rocket is declared firing | Destroy or redirect that rocket before it hits. |
| **Steal** | Any time — on your turn or an opponent's | Take 1 Grass card from a target opponent's stockpile. If a Colony Victory is declared, the steal resolves first — if the target still meets the threshold after the steal, Colony Victory confirms anyway. |
| **Sabotage** | Any time — on your turn or an opponent's | Destroy any Shield or Booster currently attached to an opponent's ship. |
| **Repair** | Any time — on your turn or an opponent's | Recover one Shield or Booster from the discard pile and attach it to an open slot on your ship. |
| **Launch** | Any time — on your turn or an opponent's | Instantly stage a rocket from your hand into your Orbit Zone, bypassing the normal Phase 4 staging window. Subject to the standard Orbit Zone cap of 2. |

---

## The Orbit Zone

- Each player has their own personal **Orbit Zone** — a visible staging area in front of them.
- Rockets placed here are **public information** — all players can see them.
- Firing rockets during Phase 2 is **optional** — you may hold them to build pressure or bluff opponents.
- **Cap: 2 rockets maximum.** If at cap, you must fire at least one in Phase 2 before staging a new one in Phase 4.
- **Targets are declared when firing, not when staging.** A rocket in the Orbit Zone has no declared target until the moment the player announces it is firing — at which point the Card Stack window opens and opponents may respond.

---

## The Card Stack

The **Card Stack** governs the order in which effects resolve when actions are declared and Special Cards are played in response. Two types of events open a Card Stack window — a rocket being fired, or a Special Card being played.

### Stack Triggers
Any of the following opens a window for all players to respond by placing a Special Card onto the stack:
1. **A player declares a rocket is firing** — during Phase 2 when a player announces their target, or when a Laser Rocket is played during Phase 4.
2. **A player plays a Special Card** — any Special Card placed on the stack opens a new window for further responses.

### How It Works
1. A triggering event occurs (rocket declared or Special Card played). That event or card sits at the bottom of the stack.
2. **Before it resolves**, any player may respond by placing a Special Card on top of the stack.
3. Each new Special Card placed opens another response window — players may keep responding until all players pass.
4. Once all players pass, the stack resolves **top to bottom** — the most recently added card or effect resolves first, working back down to the original trigger at the bottom.

### Example
- Player A declares they are firing a rocket at Player B's ship — this opens the stack.
- Player B plays an **Intercept** card on top to destroy the rocket before it hits.
- Player A responds by playing a **Sabotage** card on top of that to destroy Player B's Intercept before it resolves.
- All players pass. The stack resolves:
  - First: Player A's Sabotage resolves — Player B's Intercept is destroyed.
  - Then: Player B's Intercept fizzles — it has been destroyed and cannot resolve.
  - Finally: Player A's rocket resolves — it fires and hits Player B's ship.

### Key Rules
- **Any player may respond** to any stack event, not just the player directly affected.
- **Only Special Cards** can be added to the stack in response. Rockets, Shields, and Boosters are never placed on the stack.
- Once a card on the stack resolves, it is discarded. If its effect is no longer relevant by the time it resolves (e.g. the rocket it was meant to intercept was already destroyed by a card above it), it **fizzles** — no effect, discarded harmlessly.
- **Rocket targets are declared when firing**, not when staged — meaning a rocket in the Orbit Zone has no declared target until the moment it fires and the stack window opens.
- **Laser Rockets** resolve immediately when played but still open a stack window — opponents may respond before the Laser Rocket hits.

---

### Dealt at Game Start (Not Shuffled Into Any Pile)

| Card Type | Count | Notes |
|-----------|-------|-------|
| Ship Cards | 5 | The Baaad Omen, The Grazing Fury, The Cud Bucket, The Bleating Heart, The Herd Ship Mentality — dealt face-up at game start |

### Shared Pile (81 Cards — Shuffled at Game Start)

| Card Type | Count | Notes |
|-----------|-------|-------|
| Standard Rockets | 19 | Core attack card |
| Laser Rockets | 6 | Rare bypass — immediate hit |
| Shields | 19 | Core defense card |
| Boosters | 14 | Upgrade attachments |
| Special — Intercept | 5 | Reactive: destroy/redirect orbit rockets |
| Special — Steal | 5 | Reactive: take grass or negate Colony Victory |
| Special — Sabotage | 5 | Reactive: destroy opponent's attaching card |
| Special — Repair | 4 | Reactive: rebuild your own shield |
| Special — Launch | 4 | Open timing: instantly stage a rocket into your Orbit Zone |
| **Subtotal** | **81** | |

### Grass Pile (18 Cards — Shuffled at Game Start)

| Card Type | Count | Notes |
|-----------|-------|-------|
| Space Grass Cards | 18 | Resource / Colony Victory fuel |
| **Subtotal** | **18** | |

### Combined Total: 104 Cards

---

## Key Rules Summary

- **Hand limit:** 5 cards (discard at end of turn).
- **Slot limit:** 4 cards attached to ship at any time.
- **Orbit Zone cap:** 2 rockets max for all ships. Stage 1 rocket per turn. Firing is optional — hold to build pressure, but must fire before staging if at cap.
- **Slot replacement:** New cards can be freely played into open slots. Replacing an occupied slot requires discarding the current card — it cannot return to hand.
- **Card Stack:** Opened when a rocket is declared firing OR a Special Card is played. All players may respond by adding Special Cards on top. Once all players pass, resolves top to bottom. Fizzled effects are discarded harmlessly. Rocket targets are declared at firing, not at staging.
- **Space Grass:** Kept in a separate Grass Pile. Collected physically during Phase 3 — cards sit face-up as your stockpile. If Grass Pile is empty, skip Phase 3. Spend ability: return 2 Grass cards to the bottom of the Grass Pile during Phase 4 to draw 1 card from the Shared Pile.
- **Colony Victory:** Declared the moment your stockpile meets the threshold at the end of Phase 3. Opponents may play a Steal-type Special Card to negate it.
- **Eliminated players:** Hand and attached ship cards are discarded. Grass stockpile cards are returned to the bottom of the Grass Pile. Their ship is removed from play.

---

## Expansion Notes (Future Scope)

The base game supports 2–5 players. A future expansion could include:
- A 6th ship archetype (enabling 6 players).
- New Special Card subtypes with more complex effects.
- Strong asymmetry ship variants with fundamentally different slot/ability structures.
- Event cards or a shared board element.

---

*Document Version: 3.4 — Ship names updated to: The Baaad Omen, The Grazing Fury, The Cud Bucket, The Bleating Heart, The Herd Ship Mentality. Card distribution table updated accordingly.*
