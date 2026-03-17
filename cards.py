"""
Space Goats v2 — Card Effects Implementation

This module implements all card effects, including booster passive effects,
special card effects, and card mechanics like targeting and damage resolution.
"""

from typing import TYPE_CHECKING
from state import Card, CardType, SpecialSubtype

if TYPE_CHECKING:
    from state import GameState, Player


# ============================================================================
# Booster Effects — Passive abilities while attached to a slot
# ============================================================================

def has_booster(player: "Player", booster_name: str) -> bool:
    """Check if a player has a specific booster attached."""
    return any(slot and slot.name == booster_name for slot in player.ship.slots)


def get_orbit_zone_cap(player: "Player") -> int:
    """
    Calculate Orbit Zone cap for a player.
    Default: 2 rockets
    Modified by: Orbit Expander 3000 (+1)
    """
    cap = 2
    if has_booster(player, "Orbit Expander 3000"):
        cap += 1
    return cap


def get_draw_count_phase_1(player: "Player") -> int:
    """
    Calculate cards to draw in Phase 1.
    Default: 1 card
    Modified by: The Extra Nibble (+1)
    """
    count = 1
    if has_booster(player, "The Extra Nibble"):
        count += 1
    return count


def get_grass_collect_count_phase_3(player: "Player") -> int:
    """
    Calculate Grass cards to collect in Phase 3.
    Default: 1 card
    Modified by: The Overgrown Engine (+1)
    """
    count = 1
    if has_booster(player, "The Overgrown Engine"):
        count += 1
    return count


def get_grass_spend_cost(player: "Player") -> int:
    """
    Calculate cost of Grass Spend ability in Phase 4.
    Default: 2 Grass cards
    Modified by: The Discount Grazer (cost becomes 1)
    """
    cost = 2
    if has_booster(player, "The Discount Grazer"):
        cost = 1
    return cost


def get_grass_spend_draw_count(player: "Player") -> int:
    """
    Calculate cards drawn from Grass Spend.
    Default: 1 card
    Modified by: Double Dip Drive (becomes 2)
    """
    count = 1
    if has_booster(player, "Double Dip Drive"):
        count = 2
    return count


def is_grass_protected_by_barbed_fence(player: "Player", stack_size: int) -> bool:
    """
    Check if player's Grass is protected by The Barbed Fence.
    
    The Barbed Fence: Steal cards can only target this player's Grass
    if at least 2 Special Cards are currently on the Card Stack.
    """
    if has_booster(player, "The Barbed Fence"):
        return stack_size < 2
    return False


# ============================================================================
# Effect Resolution Functions
# ============================================================================

def effect_intercept(rocket: Card, game_state: "GameState") -> bool:
    """
    Intercept effect: Destroy or redirect the declared rocket.
    
    Returns True if rocket is successfully intercepted (destroyed).
    In simple implementation, always destroys the rocket.
    """
    return True


def effect_steal(target_player: "Player", game_state: "GameState") -> bool:
    """
    Steal effect: Take 1 Grass card from target player's stockpile.
    
    Returns True if a Grass card was successfully stolen.
    Returns False if target has no Grass (fizzles).
    
    For Colony Victory: Steal resolves first. If target still meets
    threshold after steal, Colony Victory confirms anyway.
    """
    if len(target_player.grass_stockpile) == 0:
        return False  # Fizzles
    
    # Take 1 Grass from target
    stolen_grass = target_player.grass_stockpile.pop(0)
    # Return to bottom of Grass Pile
    game_state.grass_pile.append(stolen_grass)
    return True


def effect_sabotage(target_player: "Player", target_slot_index: int, 
                   game_state: "GameState") -> bool:
    """
    Sabotage effect: Destroy any Shield or Booster in a target slot.
    
    Args:
        target_slot_index: Index of slot (0-3)
    
    Returns True if card was destroyed.
    Returns False if slot is empty (fizzles).
    """
    if not (0 <= target_slot_index <= 3):
        return False
    
    target_card = target_player.ship.slots[target_slot_index]
    if target_card is None:
        return False  # Fizzles
    
    if target_card.card_type in (CardType.SHIELD, CardType.BOOSTER):
        target_player.ship.slots[target_slot_index] = None
        game_state.discard_pile.append(target_card)
        return True
    
    return False


def effect_repair(player: "Player", card_to_recover: Card, 
                 game_state: "GameState") -> bool:
    """
    Repair effect: Recover one Shield or Booster from discard and attach to slot.
    
    Returns True if card was recovered.
    Returns False if card not in discard or no open slots (fizzles).
    """
    # Check if card is in discard pile
    if card_to_recover not in game_state.discard_pile:
        return False  # Fizzles
    
    # Check if player has open slots
    if player.ship.open_slots() == 0:
        return False  # Fizzles
    
    # Recover card from discard to first open slot
    game_state.discard_pile.remove(card_to_recover)
    for i, slot in enumerate(player.ship.slots):
        if slot is None:
            player.ship.slots[i] = card_to_recover
            break
    
    return True


def effect_launch(player: "Player", rocket_card: Card, 
                 game_state: "GameState") -> bool:
    """
    Launch effect: Instantly stage a rocket from hand into Orbit Zone.
    
    Subject to normal Orbit Zone cap (modified by Boosters).
    
    Returns True if rocket was launched.
    Returns False if Orbit Zone at cap or rocket not in hand (fizzles).
    """
    if rocket_card not in player.hand:
        return False  # Fizzles
    
    cap = get_orbit_zone_cap(player)
    if len(player.ship.orbit_zone) >= cap:
        return False  # Fizzles
    
    player.hand.remove(rocket_card)
    player.ship.orbit_zone.append(rocket_card)
    return True


# ============================================================================
# Booster Triggered Effects — Called during specific phases/events
# ============================================================================

def trigger_freeloader(owner: "Player", game_state: "GameState") -> None:
    """
    The Freeloader: When any player uses Grass Spend, owner may draw 1.
    
    Called when another player uses Grass Spend in Phase 4.
    """
    if len(game_state.shared_pile) > 0:
        card = game_state.shared_pile.pop(0)
        owner.hand.append(card)


def trigger_grief_wool(owner: "Player", game_state: "GameState") -> None:
    """
    Grief Wool: When one of owner's Shields is destroyed, draw 1 card.
    
    Called when a Shield in owner's slots is destroyed.
    """
    if len(game_state.shared_pile) > 0:
        card = game_state.shared_pile.pop(0)
        owner.hand.append(card)


def trigger_generous_gate(owner: "Player", game_state: "GameState") -> None:
    """
    The Generous Gate: When owner attaches a Shield, draw 1 card.
    
    Called after owner plays a Shield in Phase 4.
    """
    if len(game_state.shared_pile) > 0:
        card = game_state.shared_pile.pop(0)
        owner.hand.append(card)


def trigger_silver_lining(owner: "Player", game_state: "GameState") -> None:
    """
    The Silver Lining: When owner's rocket is intercepted, draw 1 card.
    
    Called when an Intercept card fizzles out the owner's rocket.
    """
    if len(game_state.shared_pile) > 0:
        card = game_state.shared_pile.pop(0)
        owner.hand.append(card)


# ============================================================================
# Rocket Targeting and Resolution
# ============================================================================

def resolve_rocket_hit(attacking_player: "Player", rocket: Card, 
                      target_player: "Player", game_state: "GameState") -> bool:
    """
    Resolve a rocket hit on target player.
    
    Targeting rules:
    - Rockets only target Shields, not Boosters
    - If no Shields remain, hit the Hull directly
    - Hitting the Hull destroys the ship
    
    Returns True if target player is eliminated.
    """
    shield_count = target_player.ship.get_shield_count()
    
    if shield_count > 0:
        # Find first Shield and destroy it
        for i, slot in enumerate(target_player.ship.slots):
            if slot and slot.card_type == CardType.SHIELD:
                target_player.ship.slots[i] = None
                game_state.discard_pile.append(slot)
                
                # Trigger Grief Wool on target if they have it
                if has_booster(target_player, "Grief Wool"):
                    trigger_grief_wool(target_player, game_state)
                
                return False  # Ship not destroyed
    else:
        # No Shields remain — hit Hull directly
        target_player.ship.hull_hp = 0
        target_player.is_eliminated = True
        return True  # Ship destroyed
    
    return False


# ============================================================================
# Card Utility Functions
# ============================================================================

def can_slot_card(card: Card) -> bool:
    """Check if a card can be slotted (Shield or Booster)."""
    return card.card_type in (CardType.SHIELD, CardType.BOOSTER)


def get_shareable_card_count_in_hand(player: "Player") -> int:
    """Count cards in hand that can be played (for Grass Spend decision)."""
    return len(player.hand)
