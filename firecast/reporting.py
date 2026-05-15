"""Console output for the Firecast test suite."""

import json

from firecast.cases import TestCase
from firecast.evaluation import EvaluationResult
from firecast.scenario import ScenarioResult


def print_suite_header() -> None:
    print("=" * 60)
    print("FIRECAST TEMPORAL REASONING TEST SUITE — Base Mem0")
    print("=" * 60)


def print_case_header(case: TestCase) -> None:
    print("\n" + "=" * 60)
    print(f"CASE: {case.name}")
    print(case.description)
    print("=" * 60)


def print_scenario_steps(result: ScenarioResult) -> None:
    case = result.case
    print(f"\n[STEP 1] {case.step1_title}")
    print("Result:", json.dumps(result.add_initial, indent=2, default=str))

    print(f"\n[STEP 2] {case.step2_title}")
    print("Result:", json.dumps(result.add_update, indent=2, default=str))

    print(f"\n[STEP 3] Querying: {case.search_query!r}")
    print("Raw search results:")
    print(json.dumps(result.search_results, indent=2, default=str))

    print(f"\n[STEP 4] All stored memories for user {case.user_id!r}:")
    print(json.dumps(result.all_memories, indent=2, default=str))


def print_evaluation(case: TestCase, evaluation: EvaluationResult) -> None:
    print("\n" + "-" * 60)
    print("EVALUATION")
    print("-" * 60)

    print(f"\nMemories returned by search: {evaluation.search_hit_count}")
    for label, snippet in evaluation.markers_in_search:
        print(f"  [{label}] {snippet}")

    print(f"\nTotal memories stored: {evaluation.total_stored}")
    print(f"{case.stale_label} returned in search: {evaluation.stale_returned}")
    print(f"{case.current_label} returned in search: {evaluation.current_returned}")

    print("\n--- VERDICT ---")
    for line in evaluation.verdict_lines:
        print(line)

    if not case.expect_additive:
        print("\nRaw add() results above tell the real story:")
        print("  Look for 'event': 'UPDATE' or conflict detection language in Step 2.")
        print("  If Step 2 shows 'ADD' (not UPDATE), base Mem0 has no temporal awareness here.")


def print_suite_summary(results: list[tuple[str, bool]]) -> None:
    print("\n" + "=" * 60)
    print("SUITE SUMMARY")
    print("=" * 60)
    passed = sum(1 for _, ok in results if ok)
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  {name}: {status}")
    print(f"\n{passed}/{len(results)} cases passed.")
