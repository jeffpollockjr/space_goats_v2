"""
Space Goats v2 — Turn Engine (5 Phases)

Implements the turn structure: Phase 1 (Draw) → Phase 2 (Orbit Resolution) →
Phase 3 (Resource/Grass) → Phase 4 (Play) → Phase 5 (End).

Each phase is a separate function. Phases are executed in strict order.
"""

from typing import TYPE_CHECKING

from state import GameState, Player, Card, CardType
from cards import (
    get_draw_count_phase_1,
    get_grass_collect_count_phase_3,
    get_orbit_zone_cap,
    get_grass_spend_cost,
    get_grass_spend_draw_count,
)
from stack import CardStack, StackEvent

if TYPE_CHECKING:
    from ai import AIPlayer


# ============================================================================
# Phase 1 — Draw
# ============================================================================

def phase_1_draw(player: Player, game_state: GameState) -> None:
    """
    Phase 1: Draw from Shared Pile.
    
    - Draw 1 card (or more if modified by boosters) from Shared Pile into hand
    - If Shared Pile empty, shuffle discard pile to form new Shared Pile
    """
    draw_count = get_draw_count_phase_1(player)
    
    for _ in range(draw_count):
        # Check if Shared Pile is empty
        if len(game_state.shared_pile) == 0:
            # Shuffle discard pile to form new Shared Pile
            if len(game_state.discard_pile) == 0:
                # No cards to draw
                break
            game_state.shared_pile = game_state.discard_pile
            game_state.discard_pile = []
            # Shuffle new Shared Pile
            import random
            random.shuffle(game_state.shared_pile)
        
        # Draw 1 card
        card = game_state.shared_pile.pop(0)
        player.hand.append(card)


# ============================================================================
# Phase 2 — Orbit Resolution
# ============================================================================

def phase_2_orbit_resolution(player: Player, game_state: GameState,
                            ai_player=None) -> None:
    """
    Phase 2: Fire or hold each rocket in Orbit Zone.
    
    - For each rocket in player's Orbit Zone, AI decides to fire or hold
    - Firing opens a Card Stack window for opponent responses
    - Held rockets stay in Orbit Zone
    - Skip this phase if no rockets in Orbit Zone
    """
    if len(player.ship.orbit_zone) == 0:
        return  # Skip phase
    
    # AI decides which rockets to fire (see ai.py for decision logic)
    if ai_player:
        ai_player.decide_phase_2_fire(player, game_state)


# ============================================================================
# Phase 3 — Resource (Grass Collection)
# ============================================================================

def phase_3_resource(player: Player, game_state: GameState) -> bool:
    """
    Phase 3: Collect Grass from Grass Pile.
    
    - Draw 1 card from Grass Pile (or more if modified) into stockpile
    - If Grass Pile empty, skip this phase entirely
    - After collecting, check if player meets Colony Victory threshold
    - Return True if Colony Victory was declared (for game.py to handle)
    """
    if len(game_state.grass_pile) == 0:
        return False  # Skip phase, no victory check
    
    collect_count = get_grass_collect_count_phase_3(player)
    
    for _ in range(collect_count):
        if len(game_state.grass_pile) == 0:
            break
        grass_card = game_state.grass_pile.pop(0)
        player.grass_stockpile.append(grass_card)
    
    # Return True to signal that Colony Victory check should occur
    return True


# ============================================================================
# Phase 4 — Play
# ============================================================================

def phase_4_play(player: Player, game_state: GameState, 
                ai_player=None) -> None:
    """
    Phase 4: Play cards from hand.
    
    AI plays cards in this order: Shields, Boosters, Rockets, Laser Rockets,
    Special Cards (open timing).
    
    - Shields attach to open ship slots
    - Boosters attach to open ship slots
    - Standard Rockets: Stage max 1 per turn into Orbit Zone (cap 2)
    - Laser Rockets: Fire immediately (open stack window)
    - Special Cards: Open timing (AI may play reactively)
    - Grass Spend: Return 2 Grass to bottom of pile, draw 1 from Shared Pile
    """
    if ai_player:
        ai_player.decide_phase_4_play(player, game_state)


# ============================================================================
# Phase 5 — End
# ============================================================================

def phase_5_end(player: Player, game_state: GameState) -> None:
    """
    Phase 5: End of turn cleanup.
    
    - Discard down to hand limit of 5 cards
    - Pass turn to next player clockwise
    """
    hand_limit = 5
    
    while len(player.hand) > hand_limit:
        # AI should choose which card to discard (simplified: discard first)
        card = player.hand.pop(0)
        game_state.discard_pile.append(card)


# ============================================================================
# Helper Functions for Card Playing
# ============================================================================

def play_shield_to_slot(player: Player, shield: Card, slot_index: int,
                       game_state: GameState) -> bool:
    """
    Play a Shield to an open slot.
    
    Returns True if successful, False if slot is occupied or invalid.
    """
    if not (0 <= slot_index <= 3):
        return False
    
    if player.ship.slots[slot_index] is not None:
        # Slot occupied — must discard current card first
        return False
    
    player.hand.remove(shield)
    player.ship.slots[slot_index] = shield
    
    # Trigger The Generous Gate if player has it
    from cards import has_booster, trigger_generous_gate
    if has_booster(player, "The Generous Gate"):
        trigger_generous_gate(player, game_state)
    
    return True


def play_booster_to_slot(player: Player, booster: Card, slot_index: int,
                        game_state: GameState) -> bool:
    """
    Play a Booster to an open or occupied slot.
    
    If slot is occupied, the current card is discarded (not returned to hand).
    Returns True if successful.
    """
    if not (0 <= slot_index <= 3):
        return False
    
    # If slot is occupied, discard the current card
    if player.ship.slots[slot_index] is not None:
        old_card = player.ship.slots[slot_index]
        
        # Check if old card has The Revolving Hoof (returns to hand instead)
        from cards import has_booster
        if has_booster(player, "The Revolving Hoof"):
            player.hand.append(old_card)
        else:
            game_state.discard_pile.append(old_card)
    
    player.hand.remove(booster)
    player.ship.slots[slot_index] = booster
    
    return True


def stage_rocket_to_orbit(player: Player, rocket: Card,
                         game_state: GameState) -> bool:
    """
    Stage a Standard Rocket to Orbit Zone.
    
    Subject to Orbit Zone cap (default 2, modified by Boosters).
    Returns True if successful, False if at cap or not a valid rocket.
    """
    if rocket.card_type != CardType.STANDARD_ROCKET:
        return False
    
    cap = get_orbit_zone_cap(player)
    if len(player.ship.orbit_zone) >= cap:
        return False  # At cap
    
    player.hand.remove(rocket)
    player.ship.orbit_zone.append(rocket)
    return True


def fire_laser_rocket(player: Player, laser_rocket: Card, 
                     target_player: Player,
                     game_state: GameState) -> None:
    """
    Fire a Laser Rocket immediately.
    
    Laser Rockets bypass the Orbit Zone but still open a Card Stack window
    for opponent responses.
    
    This function creates the stack event and opens the window.
    """
    if laser_rocket.card_type != CardType.LASER_ROCKET:
        return
    
    # Remove from hand
    player.hand.remove(laser_rocket)
    
    # Create stack event
    event = StackEvent(
        trigger_type="rocket_fired",
        source_player=player,
        target_player=target_player,
        card=laser_rocket
    )
    
    # Push to stack and open response window
    game_state.card_stack.push(event)


def grass_spend(player: Player, game_state: GameState) -> None:
    """
    Execute Grass Spend ability.
    
    - Return N Grass cards from stockpile to bottom of Grass Pile
    - Draw M cards from Shared Pile (N and M modified by boosters)
    
    Cost: 2 Grass normally, 1 if modified by The Discount Grazer
    Draw: 1 card normally, 2 if modified by Double Dip Drive
    """
    from cards import trigger_freeloader
    
    cost = get_grass_spend_cost(player)
    draw_count = get_grass_spend_draw_count(player)
    
    # Check if player has enough Grass
    if len(player.grass_stockpile) < cost:
        return  # Cannot spend
    
    # Return Grass to bottom of Grass Pile
    for _ in range(cost):
        if len(player.grass_stockpile) > 0:
            grass = player.grass_stockpile.pop(0)
            game_state.grass_pile.append(grass)
    
    # Draw cards from Shared Pile
    for _ in range(draw_count):
        if len(game_state.shared_pile) == 0:
            # Shuffle discard
            if len(game_state.discard_pile) > 0:
                game_state.shared_pile = game_state.discard_pile
                game_state.discard_pile = []
                import random
                random.shuffle(game_state.shared_pile)
        
        if len(game_state.shared_pile) > 0:
            card = game_state.shared_pile.pop(0)
            player.hand.append(card)
    
    # Trigger The Freeloader on all other players
    for other_player in game_state.get_other_players():
        from cards import has_booster
        if has_booster(other_player, "The Freeloader"):
            trigger_freeloader(other_player, game_state)


def peek_shared_pile(player: Player, game_state: GameState) -> Card:
    """
    Peek at the top card of Shared Pile (The Nosy Snout ability).
    
    Returns the card or None if pile is empty.
    """
    if len(game_state.shared_pile) > 0:
        return game_state.shared_pile[0]
    return None


def peek_opponent_hand(player: Player, opponent: Player) -> list:
    """
    Peek at opponent's hand (The Periscope Horn ability).
    
    Returns a copy of the opponent's hand.
    """
    return opponent.hand.copy()
