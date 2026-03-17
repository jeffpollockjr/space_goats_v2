"""
Space Goats v2 — Deck and Pile Construction

This module builds the Shared Pile (81 cards) and Grass Pile (18 cards).
All card definitions come from space_goats_v2_cards.md.
"""

import random
from typing import List

from state import Card, CardType, SpecialSubtype


# ============================================================================
# Card Definitions — All 104 cards based on space_goats_v2_cards.md
# ============================================================================

STANDARD_ROCKETS = [
    Card("Barnyard Ballistic", CardType.STANDARD_ROCKET),
    Card("Hoof-Seeking Missile", CardType.STANDARD_ROCKET),
    Card("The Tin Can Torpedo", CardType.STANDARD_ROCKET),
    Card("Bleat and Destroy", CardType.STANDARD_ROCKET),
    Card("Cosmic Headbutt", CardType.STANDARD_ROCKET),
    Card("The Wool Stripper", CardType.STANDARD_ROCKET),
    Card("Pasture Pounder", CardType.STANDARD_ROCKET),
    Card("Billy's Bad Idea", CardType.STANDARD_ROCKET),
    Card("Galactic Gut Buster", CardType.STANDARD_ROCKET),
    Card("The Stinky Payload", CardType.STANDARD_ROCKET),
    Card("Interstellar Ramrod", CardType.STANDARD_ROCKET),
    Card("The Hay Maker", CardType.STANDARD_ROCKET),
    Card("Udder Devastation", CardType.STANDARD_ROCKET),
    Card("Meteor Bleater", CardType.STANDARD_ROCKET),
    Card("The Grass Burner", CardType.STANDARD_ROCKET),
    Card("Stellar Ram Rod", CardType.STANDARD_ROCKET),
    Card("Space Manure Missile", CardType.STANDARD_ROCKET),
    Card("Cloven Cannonball", CardType.STANDARD_ROCKET),
    Card("The Nanny Nuke", CardType.STANDARD_ROCKET),
]

LASER_ROCKETS = [
    Card("Flash Bleat", CardType.LASER_ROCKET),
    Card("Hyperspace Headbutt", CardType.LASER_ROCKET),
    Card("The Speed Goat Special", CardType.LASER_ROCKET),
    Card("Warp Wool Burner", CardType.LASER_ROCKET),
    Card("Instant Incineration", CardType.LASER_ROCKET),
    Card("Zero Gravity Zapper", CardType.LASER_ROCKET),
]

SHIELDS = [
    Card("The Tin Fleece", CardType.SHIELD),
    Card("Bubble Wrap Bulkhead", CardType.SHIELD),
    Card("The Astro Bale", CardType.SHIELD),
    Card("Hoof Plate Alpha", CardType.SHIELD),
    Card("The Wool Wall", CardType.SHIELD),
    Card("Barnyard Barrier", CardType.SHIELD),
    Card("Cosmic Cowbell", CardType.SHIELD),
    Card("The Nanny Guard", CardType.SHIELD),
    Card("Bleat Deflector", CardType.SHIELD),
    Card("Herd Instinct Hull", CardType.SHIELD),
    Card("Galactic Grazing Guard", CardType.SHIELD),
    Card("The Cud Buckler", CardType.SHIELD),
    Card("Interstellar Udder Cover", CardType.SHIELD),
    Card("Billy Proof Plating", CardType.SHIELD),
    Card("The Pasture Pauldron", CardType.SHIELD),
    Card("Meteor Mantle", CardType.SHIELD),
    Card("Straw Reinforced Steel", CardType.SHIELD),
    Card("Hoof Plate Omega", CardType.SHIELD),
    Card("The Last Resort Layer", CardType.SHIELD),
]

BOOSTERS = [
    Card("The Extra Nibble", CardType.BOOSTER),
    Card("Orbit Expander 3000", CardType.BOOSTER),
    Card("The Discount Grazer", CardType.BOOSTER),
    Card("The Nosy Snout", CardType.BOOSTER),
    Card("The Freeloader", CardType.BOOSTER),
    Card("Grief Wool", CardType.BOOSTER),
    Card("The Generous Gate", CardType.BOOSTER),
    Card("The Panic Button", CardType.BOOSTER),
    Card("The Overgrown Engine", CardType.BOOSTER),
    Card("The Barbed Fence", CardType.BOOSTER),
    Card("Double Dip Drive", CardType.BOOSTER),
    Card("The Periscope Horn", CardType.BOOSTER),
    Card("The Silver Lining", CardType.BOOSTER),
    Card("The Revolving Hoof", CardType.BOOSTER),
]

SPECIAL_INTERCEPT = [
    Card("Not In My Pasture", CardType.SPECIAL, SpecialSubtype.INTERCEPT),
    Card("The Hoof Block", CardType.SPECIAL, SpecialSubtype.INTERCEPT),
    Card("Wool Over Your Eyes", CardType.SPECIAL, SpecialSubtype.INTERCEPT),
    Card("The Goat Stare", CardType.SPECIAL, SpecialSubtype.INTERCEPT),
    Card("Gravity's Goat", CardType.SPECIAL, SpecialSubtype.INTERCEPT),
]

SPECIAL_STEAL = [
    Card("The Midnight Munch", CardType.SPECIAL, SpecialSubtype.STEAL),
    Card("Hoof in the Cookie Jar", CardType.SPECIAL, SpecialSubtype.STEAL),
    Card("The Sneaky Graze", CardType.SPECIAL, SpecialSubtype.STEAL),
    Card("Galactic Grass Grab", CardType.SPECIAL, SpecialSubtype.STEAL),
    Card("Not Your Colony", CardType.SPECIAL, SpecialSubtype.STEAL),
]

SPECIAL_SABOTAGE = [
    Card("Chew Through It", CardType.SPECIAL, SpecialSubtype.SABOTAGE),
    Card("The Jealous Headbutt", CardType.SPECIAL, SpecialSubtype.SABOTAGE),
    Card("Cosmic Vandalism", CardType.SPECIAL, SpecialSubtype.SABOTAGE),
    Card("Horn Meets Hardware", CardType.SPECIAL, SpecialSubtype.SABOTAGE),
    Card("What's Yours Is Gone", CardType.SPECIAL, SpecialSubtype.SABOTAGE),
]

SPECIAL_REPAIR = [
    Card("Duct Tape and Dreams", CardType.SPECIAL, SpecialSubtype.REPAIR),
    Card("The Second Fleece", CardType.SPECIAL, SpecialSubtype.REPAIR),
    Card("Salvage Goat", CardType.SPECIAL, SpecialSubtype.REPAIR),
    Card("Good As New (It Is Not)", CardType.SPECIAL, SpecialSubtype.REPAIR),
]

SPECIAL_LAUNCH = [
    Card("Surprise Surprise", CardType.SPECIAL, SpecialSubtype.LAUNCH),
    Card("The Sneak Bleat", CardType.SPECIAL, SpecialSubtype.LAUNCH),
    Card("Hoof on the Trigger", CardType.SPECIAL, SpecialSubtype.LAUNCH),
    Card("Unscheduled Departure", CardType.SPECIAL, SpecialSubtype.LAUNCH),
]

SPACE_GRASS = [
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
    Card("Space Grass", CardType.SPACE_GRASS),
]

SHIPS = [
    Card("The Baaad Omen", CardType.STANDARD_ROCKET),
    Card("The Grazing Fury", CardType.STANDARD_ROCKET),
    Card("The Cud Bucket", CardType.STANDARD_ROCKET),
    Card("The Bleating Heart", CardType.STANDARD_ROCKET),
    Card("The Herd Ship Mentality", CardType.STANDARD_ROCKET),
]


# ============================================================================
# Pile Construction
# ============================================================================

def build_shared_pile() -> List[Card]:
    """
    Build the Shared Pile (81 cards).
    
    Composition:
    - 19 Standard Rockets
    - 6 Laser Rockets
    - 19 Shields
    - 14 Boosters
    - 5 Intercept Special Cards
    - 5 Steal Special Cards
    - 5 Sabotage Special Cards
    - 4 Repair Special Cards
    - 4 Launch Special Cards
    = 81 total
    """
    shared_pile = (
        STANDARD_ROCKETS.copy() +
        LASER_ROCKETS.copy() +
        SHIELDS.copy() +
        BOOSTERS.copy() +
        SPECIAL_INTERCEPT.copy() +
        SPECIAL_STEAL.copy() +
        SPECIAL_SABOTAGE.copy() +
        SPECIAL_REPAIR.copy() +
        SPECIAL_LAUNCH.copy()
    )
    return shared_pile


def build_grass_pile() -> List[Card]:
    """Build the Grass Pile (18 Space Grass cards)."""
    return SPACE_GRASS.copy()


def build_ship_cards() -> List[Card]:
    """Build the 5 Ship Cards (dealt at setup, never shuffled)."""
    return SHIPS.copy()


def create_game_piles(random_seed: int = None) -> tuple:
    """
    Create and shuffle the game piles.
    
    Returns:
        (shared_pile, grass_pile, ship_cards) — all shuffled except ship_cards
    """
    if random_seed is not None:
        random.seed(random_seed)
    
    shared_pile = build_shared_pile()
    grass_pile = build_grass_pile()
    ship_cards = build_ship_cards()
    
    random.shuffle(shared_pile)
    random.shuffle(grass_pile)
    
    return shared_pile, grass_pile, ship_cards
