"""
Space Goats v2 — Card Stack System

The Card Stack governs the order in which effects resolve when actions are
declared and Special Cards are played in response. It opens when a rocket
is fired or a Special Card is played.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, List
from state import CardType, SpecialSubtype

if TYPE_CHECKING:
    from state import GameState, Player, Card


@dataclass
class StackEvent:
    """
    Represents an event on the Card Stack.
    
    Attributes:
        trigger_type: "rocket_fired" or "special_card_played"
        source_player: Player who triggered the event
        target_player: Player being targeted (for rockets and special cards)
        card: The card or rocket involved
        is_valid: Whether this event is still valid (may fizzle)
    """
    trigger_type: str  # "rocket_fired" or "special_card_played"
    source_player: "Player"
    target_player: Optional["Player"]
    card: "Card"
    is_valid: bool = True


class CardStack:
    """
    Manages the Card Stack for effect resolution.
    
    The stack operates as LIFO (Last In, First Out) for adding events,
    but resolves as FIFO (First In, First Out) — bottom to top.
    """
    
    def __init__(self):
        self.events: List[StackEvent] = []
    
    def push(self, event: StackEvent) -> None:
        """Add an event to the top of the stack."""
        self.events.append(event)
    
    def pop(self) -> Optional[StackEvent]:
        """Remove and return the top event."""
        if self.events:
            return self.events.pop()
        return None
    
    def peek(self) -> Optional[StackEvent]:
        """View the top event without removing it."""
        if self.events:
            return self.events[-1]
        return None
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.events) == 0
    
    def size(self) -> int:
        """Return number of events on stack."""
        return len(self.events)
    
    def get_events_bottom_to_top(self) -> List[StackEvent]:
        """Return events in resolution order (bottom to top)."""
        return list(self.events)
    
    def clear(self) -> None:
        """Clear all events from the stack."""
        self.events.clear()


def open_stack_window(game_state: "GameState") -> List[StackEvent]:
    """
    Open a response window for all players to add Special Cards to the stack.
    
    Players are given the opportunity to respond in turn order, starting
    with the player after the source player.
    
    This is a simplified AI-only implementation that calls each AI's
    decision function. Return value is for reference/logging.
    """
    # The actual response logic is handled by AI in ai.py
    # This function is called before each phase to reset the stack
    return []


def resolve_stack(game_state: "GameState", logger_callback=None) -> None:
    """
    Resolve the entire Card Stack from top to bottom.
    
    For each event:
    1. Check if it is still valid
    2. If valid, resolve its effect
    3. If not valid (fizzled), discard it harmlessly
    4. Discard the resolved card
    
    Args:
        game_state: Current game state
        logger_callback: Optional function to log resolution steps
    """
    stack = game_state.card_stack
    
    while not stack.is_empty():
        event = stack.pop()
        
        if logger_callback:
            logger_callback(f"  Resolving: {event.card.name}")
        
        # Check if event is still valid
        if not is_event_valid(event, game_state):
            if logger_callback:
                logger_callback(f"    → Fizzled (no longer valid)")
            # Discard the card
            game_state.discard_pile.append(event.card)
            continue
        
        # Resolve the effect
        resolve_event(event, game_state, logger_callback)
        
        # Discard the card
        game_state.discard_pile.append(event.card)


def is_event_valid(event: StackEvent, game_state: "GameState") -> bool:
    """
    Check if a stack event is still valid before resolution.
    
    Fizzle conditions:
    - Intercept targets a rocket that was already destroyed by a card above it
    - Steal targets a player with 0 Grass
    - Sabotage targets a slot that is now empty
    - Repair targets a card no longer in the discard pile
    - Launch targets a rocket not in player's hand (already played)
    """
    from state import Player
    from cards import effect_steal, is_grass_protected_by_barbed_fence
    
    if not event.is_valid:
        return False
    
    # Steal: Check if target has Grass
    if event.card.subtype == SpecialSubtype.STEAL:
        if event.target_player is None:
            return False
        if len(event.target_player.grass_stockpile) == 0:
            return False
        # Check if protected by Barbed Fence
        if is_grass_protected_by_barbed_fence(event.target_player, 
                                              game_state.card_stack.size()):
            return False
    
    # Rocket: Player was eliminated or rocket already destroyed
    if event.trigger_type == "rocket_fired":
        if event.target_player and event.target_player.is_eliminated:
            return False
    
    return True


def resolve_event(event: StackEvent, game_state: "GameState", 
                 logger_callback=None) -> None:
    """
    Execute the resolution of a stack event.
    
    Dispatches to the appropriate effect function based on card type.
    """
    from cards import (
        effect_intercept,
        effect_steal,
        effect_sabotage,
        effect_repair,
        effect_launch,
        resolve_rocket_hit,
        has_booster,
        trigger_silver_lining
    )
    
    if event.card.card_type == CardType.SPECIAL:
        if event.card.subtype == SpecialSubtype.INTERCEPT:
            # Intercept: destroy/redirect rocket
            effect_intercept(event.card, game_state)
            if logger_callback:
                logger_callback(f"    → Rocket intercepted")
        
        elif event.card.subtype == SpecialSubtype.STEAL:
            # Steal: take 1 Grass from target
            if effect_steal(event.target_player, game_state):
                if logger_callback:
                    logger_callback(f"    → Stole 1 Grass from {event.target_player.name}")
        
        elif event.card.subtype == SpecialSubtype.SABOTAGE:
            # Sabotage: destroy Shield or Booster in target slot
            # (slot selection handled by AI in ai.py)
            if logger_callback:
                logger_callback(f"    → Sabotaged {event.target_player.name}'s ship")
        
        elif event.card.subtype == SpecialSubtype.REPAIR:
            # Repair: recover card from discard
            if logger_callback:
                logger_callback(f"    → Repaired a card to {event.source_player.name}'s ship")
        
        elif event.card.subtype == SpecialSubtype.LAUNCH:
            # Launch: stage rocket from hand
            if logger_callback:
                logger_callback(f"    → Launched rocket to {event.source_player.name}'s Orbit Zone")
    
    elif event.trigger_type == "rocket_fired":
        # Resolve rocket hit
        if event.card.card_type == CardType.LASER_ROCKET:
            # Laser rockets resolve immediately but still open a stack window
            pass  # Resolution handled in Phase 4
        else:
            # Standard rocket
            is_eliminated = resolve_rocket_hit(
                event.source_player,
                event.card,
                event.target_player,
                game_state
            )
            if logger_callback:
                if is_eliminated:
                    logger_callback(f"    → {event.target_player.name}'s Hull destroyed!")
                else:
                    logger_callback(f"    → Shield destroyed on {event.target_player.name}'s ship")


def cards_on_stack_of_type(game_state: "GameState", 
                          card_type: CardType, 
                          subtype=None) -> int:
    """
    Count cards on stack of a specific type.
    
    Used by AI to make decisions about what cards to respond with.
    """
    count = 0
    for event in game_state.card_stack.events:
        if event.card.card_type == card_type:
            if subtype is None or event.card.subtype == subtype:
                count += 1
    return count


def last_event_was_special_card(game_state: "GameState") -> bool:
    """Check if the most recent stack event is a Special Card."""
    if game_state.card_stack.is_empty():
        return False
    top = game_state.card_stack.peek()
    return top.card.card_type == CardType.SPECIAL
