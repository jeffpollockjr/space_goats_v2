"""
Space Goats v2 — Game State Data Structures

This module defines all core game objects: Card, Ship, Player, and GameState.
Everything else in the simulation depends on these structures.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from stack import CardStack


class CardType(Enum):
    """Card type classification."""
    STANDARD_ROCKET = "standard_rocket"
    LASER_ROCKET = "laser_rocket"
    SHIELD = "shield"
    BOOSTER = "booster"
    SPACE_GRASS = "space_grass"
    SPECIAL = "special"


class SpecialSubtype(Enum):
    """Special card subtypes."""
    INTERCEPT = "intercept"
    STEAL = "steal"
    SABOTAGE = "sabotage"
    REPAIR = "repair"
    LAUNCH = "launch"


@dataclass
class Card:
    """
    Represents a single card.
    
    Attributes:
        name: Card name
        card_type: CardType enum value
        subtype: SpecialSubtype (for Special cards) or None
        effect: Effect description (for reference)
    """
    name: str
    card_type: CardType
    subtype: Optional[SpecialSubtype] = None
    effect: str = ""
    
    def __repr__(self) -> str:
        return f"Card({self.name})"
    
    def __eq__(self, other):
        return isinstance(other, Card) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)


@dataclass
class Ship:
    """
    Represents a player's ship.
    
    Attributes:
        name: Ship name
        hull_hp: Hull hit points (always 1)
        slots: 4 upgrade slots (Shields or Boosters)
        orbit_zone: Rockets staged here (max 2 or modified by Boosters)
    """
    name: str
    hull_hp: int = 1
    slots: List[Optional[Card]] = field(default_factory=lambda: [None, None, None, None])
    orbit_zone: List[Card] = field(default_factory=list)
    
    def __repr__(self) -> str:
        return f"Ship({self.name})"
    
    def open_slots(self) -> int:
        """Return number of open slots."""
        return sum(1 for slot in self.slots if slot is None)
    
    def get_shield_count(self) -> int:
        """Return number of attached Shields."""
        return sum(1 for slot in self.slots if slot and slot.card_type == CardType.SHIELD)
    
    def get_boosters(self) -> List[Card]:
        """Return list of attached Boosters."""
        return [slot for slot in self.slots if slot and slot.card_type == CardType.BOOSTER]


@dataclass
class Player:
    """
    Represents a player in the game.
    
    Attributes:
        name: Player name
        ship: Ship object
        hand: Cards in hand (max 5)
        grass_stockpile: Face-up Grass cards collected (for Colony Victory)
        is_eliminated: True if ship is destroyed
        used_panic_button: Tracks if Panic Button booster was used (once per game)
    """
    name: str
    ship: Ship
    hand: List[Card] = field(default_factory=list)
    grass_stockpile: List[Card] = field(default_factory=list)
    is_eliminated: bool = False
    used_panic_button: bool = False
    
    def __repr__(self) -> str:
        return f"Player({self.name})"


@dataclass
class GameState:
    """
    Represents the complete game state.
    
    Attributes:
        players: List of Player objects
        shared_pile: Cards available for drawing (Rockets, Shields, Boosters, Special)
        grass_pile: Grass cards for Resource Phase collection
        discard_pile: Cards that have been played/destroyed
        card_stack: Active Card Stack for resolving effects (CardStack object)
        current_player_index: Index of player whose turn it is
        current_phase: Phase number (1-5)
        turn_count: Total turns played
    """
    players: List[Player]
    shared_pile: List[Card] = field(default_factory=list)
    grass_pile: List[Card] = field(default_factory=list)
    discard_pile: List[Card] = field(default_factory=list)
    card_stack: Optional["CardStack"] = None  # Will be initialized in game.py
    current_player_index: int = 0
    current_phase: int = 1
    turn_count: int = 0
    
    def get_current_player(self) -> Player:
        """Return the player whose turn it is."""
        return self.players[self.current_player_index]
    
    def get_other_players(self, exclude_eliminated: bool = True) -> List[Player]:
        """Return list of all players except the current player."""
        others = [p for i, p in enumerate(self.players) if i != self.current_player_index]
        if exclude_eliminated:
            others = [p for p in others if not p.is_eliminated]
        return others
    
    def get_active_players(self) -> List[Player]:
        """Return list of non-eliminated players."""
        return [p for p in self.players if not p.is_eliminated]
    
    def count_active_players(self) -> int:
        """Return number of non-eliminated players."""
        return len(self.get_active_players())
