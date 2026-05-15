"""Run a test case against Mem0: add conflicting facts, search, list stored memories."""

from dataclasses import dataclass

from mem0 import Memory

from firecast.cases import TestCase


@dataclass
class ScenarioResult:
    case: TestCase
    add_initial: dict
    add_update: dict
    search_results: dict
    all_memories: dict


def run_scenario(memory: Memory, case: TestCase) -> ScenarioResult:
    add_initial = memory.add(
        case.initial_memory,
        user_id=case.user_id,
        metadata=case.initial_metadata or None,
    )
    add_update = memory.add(
        case.update_memory,
        user_id=case.user_id,
        metadata=case.update_metadata or None,
    )
    search_results = memory.search(case.search_query, user_id=case.user_id)
    all_memories = memory.get_all(user_id=case.user_id)
    return ScenarioResult(
        case=case,
        add_initial=add_initial,
        add_update=add_update,
        search_results=search_results,
        all_memories=all_memories,
    )
