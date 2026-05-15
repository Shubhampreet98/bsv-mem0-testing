"""Test case definitions for temporal reasoning evaluation."""

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class TestCase:
    name: str
    description: str
    user_id: str
    initial_memory: str
    update_memory: str
    search_query: str
    stale_markers: Tuple[str, ...]
    current_markers: Tuple[str, ...]
    initial_metadata: Dict[str, Any] = field(default_factory=dict)
    update_metadata: Dict[str, Any] = field(default_factory=dict)
    stale_label: str = "STALE"
    current_label: str = "CURRENT"
    expect_additive: bool = False
    step1_title: str = "Adding initial memory"
    step2_title: str = "Adding update memory"


FIRE_DISTANCE = TestCase(
    name="fire_distance",
    description="Wildfire distance escalates from 5 miles to 2 miles",
    user_id="firecast_fire_user",
    initial_memory=(
        "The wildfire is currently 5 miles away from my house. "
        "Winds are calm. Evacuation advisory is in effect."
    ),
    update_memory=(
        "The wildfire is now only 2 miles from my house. "
        "Winds have picked up. Mandatory evacuation order issued."
    ),
    search_query="How far is the fire from my house?",
    stale_markers=("5 miles", "5-mile", "five miles"),
    current_markers=("2 miles", "2-mile", "two miles"),
    initial_metadata={"event": "fire_update", "distance_miles": 5, "ts": "T+0"},
    update_metadata={"event": "fire_update", "distance_miles": 2, "ts": "T+30min"},
    step1_title="Adding initial memory: fire is 5 miles away",
    step2_title="Adding update: fire has moved to 2 miles away",
)

LOCATION_CHANGE = TestCase(
    name="location_change",
    description="User relocates from Austin to Denver",
    user_id="firecast_location_user",
    initial_memory="I live in Austin, Texas and work downtown.",
    update_memory="I moved to Denver, Colorado last month and love the mountains.",
    search_query="Where do I live?",
    stale_markers=("Austin",),
    current_markers=("Denver",),
    initial_metadata={"event": "location", "city": "Austin"},
    update_metadata={"event": "location", "city": "Denver"},
    step1_title="Adding initial memory: lives in Austin",
    step2_title="Adding update: moved to Denver",
)

BUDGET_UPDATE = TestCase(
    name="budget_update",
    description="Project budget increases from $10k to $50k",
    user_id="firecast_budget_user",
    initial_memory="My project budget is $10,000 for this quarter.",
    update_memory="Finance approved a revised project budget of $50,000 for this quarter.",
    search_query="What is my project budget?",
    stale_markers=("$10,000", "$10k", "10,000"),
    current_markers=("$50,000", "$50k", "50,000"),
    initial_metadata={"event": "budget", "amount": 10000},
    update_metadata={"event": "budget", "amount": 50000},
    step1_title="Adding initial memory: budget is $10k",
    step2_title="Adding update: budget revised to $50k",
)

ALLERGY_CONTRADICTION = TestCase(
    name="allergy_contradiction",
    description="Allergy to peanuts vs now eating peanut butter",
    user_id="firecast_allergy_user",
    initial_memory="I am allergic to peanuts and avoid all peanut products.",
    update_memory="My doctor cleared me and I now eat peanut butter regularly.",
    search_query="Can I eat peanuts or peanut butter?",
    stale_markers=("allergic to peanuts", "avoid all peanut"),
    current_markers=("eat peanut butter", "eat peanuts"),
    initial_metadata={"event": "health", "allergy": "peanuts"},
    update_metadata={"event": "health", "allergy": "cleared"},
    step1_title="Adding initial memory: allergic to peanuts",
    step2_title="Adding update: cleared to eat peanut butter",
)

ADDITIVE_CONTROL = TestCase(
    name="additive_control",
    description="Non-conflicting preferences (hiking + coffee) should coexist",
    user_id="firecast_additive_user",
    initial_memory="I love hiking on weekends in the mountains.",
    update_memory="I also love drinking coffee every morning.",
    search_query="What are my hobbies and interests?",
    stale_markers=("hiking",),
    current_markers=("coffee",),
    expect_additive=True,
    stale_label="FIRST",
    current_label="SECOND",
    initial_metadata={"event": "preference", "topic": "hiking"},
    update_metadata={"event": "preference", "topic": "coffee"},
    step1_title="Adding initial memory: likes hiking",
    step2_title="Adding second fact: likes coffee (non-conflicting)",
)

ALL_CASES: Tuple[TestCase, ...] = (
    FIRE_DISTANCE,
    LOCATION_CHANGE,
    BUDGET_UPDATE,
    ALLERGY_CONTRADICTION,
    ADDITIVE_CONTROL,
)

CASES_BY_NAME = {case.name: case for case in ALL_CASES}
