"""Evaluate scenario outcomes against temporal reasoning criteria."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from firecast.cases import TestCase
from firecast.scenario import ScenarioResult


@dataclass
class EvaluationResult:
    case_name: str
    search_hit_count: int
    markers_in_search: list[tuple[str, str]]
    total_stored: int
    stale_returned: bool
    current_returned: bool
    passed: bool
    verdict_lines: list[str]


def _extract_results(payload: Union[dict, list]) -> list:
    if isinstance(payload, dict):
        return payload.get("results", payload)
    return payload


def _text_matches_markers(text: str, markers: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(marker.lower() in lower for marker in markers)


def _find_markers_in_search(
    search_hits: list, case: TestCase
) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for hit in search_hits:
        text = hit.get("memory", "")
        if _text_matches_markers(text, case.stale_markers):
            found.append((case.stale_label, text[:80]))
        if _text_matches_markers(text, case.current_markers):
            found.append((case.current_label, text[:80]))
    return found


def evaluate(result: ScenarioResult) -> EvaluationResult:
    case = result.case
    search_hits = _extract_results(result.search_results)
    all_stored = _extract_results(result.all_memories)
    markers_in_search = _find_markers_in_search(search_hits, case)

    stale_returned = any(label == case.stale_label for label, _ in markers_in_search)
    current_returned = any(label == case.current_label for label, _ in markers_in_search)
    total_stored = len(all_stored)

    verdict_lines, passed = _build_verdict(
        case, stale_returned, current_returned, total_stored
    )

    return EvaluationResult(
        case_name=case.name,
        search_hit_count=len(search_hits),
        markers_in_search=markers_in_search,
        total_stored=total_stored,
        stale_returned=stale_returned,
        current_returned=current_returned,
        passed=passed,
        verdict_lines=verdict_lines,
    )


def _build_verdict(
    case: TestCase,
    stale_returned: bool,
    current_returned: bool,
    total_stored: int,
) -> tuple[list[str], bool]:
    if case.expect_additive:
        if stale_returned and current_returned and total_stored >= 2:
            return (
                [
                    "PASS: Both non-conflicting facts returned and stored.",
                    "      Mem0 correctly kept additive memories separate.",
                ],
                True,
            )
        if total_stored < 2:
            return (
                [
                    "FAIL: Expected at least 2 stored memories for additive facts.",
                    f"      Found {total_stored}.",
                ],
                False,
            )
        return (
            [
                "FAIL: Additive control — both facts should appear in search results.",
                f"      {case.stale_label} in search: {stale_returned}",
                f"      {case.current_label} in search: {current_returned}",
            ],
            False,
        )

    if stale_returned and current_returned:
        return (
            [
                "FAIL: Both stale and current facts returned. No conflict resolution.",
                "      Mem0 treated this as additive, not superseding.",
            ],
            False,
        )
    if stale_returned and not current_returned:
        return (
            ["FAIL: Only stale fact returned. Update was not surfaced."],
            False,
        )
    if not stale_returned and current_returned:
        lines = [
            "PASS (conditional): Only current fact returned in search.",
            "      Check Step 2 — did Mem0 use UPDATE or only rank the newer embedding higher?",
        ]
        if total_stored > 1:
            lines.append(
                "      WARNING: Both facts still stored; pass is fragile (ranking-dependent)."
            )
        return (lines, True)
    return (["INCONCLUSIVE: Neither fact clearly returned in search."], False)
