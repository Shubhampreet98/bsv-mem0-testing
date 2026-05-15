"""Write Firecast test results to JSON and Markdown files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from firecast.cases import TestCase
from firecast.client import PROJECT_ROOT
from firecast.evaluation import EvaluationResult
from firecast.scenario import ScenarioResult

DEFAULT_OUTPUT_STEM = PROJECT_ROOT / "output" / "firecast_results"


@dataclass
class CaseRun:
    scenario: ScenarioResult
    evaluation: EvaluationResult


@dataclass
class SuiteRun:
    cases: list[CaseRun]
    run_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.run_at is None:
            self.run_at = datetime.now(timezone.utc)

    @property
    def passed_count(self) -> int:
        return sum(1 for run in self.cases if run.evaluation.passed)

    @property
    def total_count(self) -> int:
        return len(self.cases)


def _add_events(payload: dict) -> list[str]:
    events: list[str] = []
    for item in payload.get("results", []):
        event = item.get("event")
        if event:
            events.append(str(event))
    return events


def _case_record(run: CaseRun) -> dict[str, Any]:
    case = run.scenario.case
    ev = run.evaluation
    return {
        "name": case.name,
        "description": case.description,
        "user_id": case.user_id,
        "search_query": case.search_query,
        "expect_additive": case.expect_additive,
        "passed": ev.passed,
        "verdict": ev.verdict_lines,
        "evaluation": {
            "search_hit_count": ev.search_hit_count,
            "total_stored": ev.total_stored,
            "stale_returned": ev.stale_returned,
            "current_returned": ev.current_returned,
            "markers_in_search": [
                {"label": label, "snippet": snippet}
                for label, snippet in ev.markers_in_search
            ],
        },
        "steps": {
            "add_initial": run.scenario.add_initial,
            "add_update": run.scenario.add_update,
            "add_initial_events": _add_events(run.scenario.add_initial),
            "add_update_events": _add_events(run.scenario.add_update),
            "search_results": run.scenario.search_results,
            "all_memories": run.scenario.all_memories,
        },
    }


def suite_to_dict(suite: SuiteRun) -> dict[str, Any]:
    return {
        "suite": "firecast_temporal_reasoning",
        "product": "Mem0 (base)",
        "run_at": suite.run_at.isoformat() if suite.run_at else None,
        "summary": {
            "passed": suite.passed_count,
            "total": suite.total_count,
            "all_passed": suite.passed_count == suite.total_count,
        },
        "cases": [_case_record(run) for run in suite.cases],
    }


def _status(passed: bool) -> str:
    return "PASS" if passed else "FAIL"


def _format_markers(ev: EvaluationResult) -> str:
    if not ev.markers_in_search:
        return "_None matched in search results._\n"
    lines = []
    for label, snippet in ev.markers_in_search:
        lines.append(f"- **[{label}]** {snippet}")
    return "\n".join(lines) + "\n"


def _format_case_section(run: CaseRun) -> str:
    case = run.scenario.case
    ev = run.evaluation
    status = _status(ev.passed)
    initial_events = _add_events(run.scenario.add_initial) or ["—"]
    update_events = _add_events(run.scenario.add_update) or ["—"]

    verdict = "\n".join(f"> {line.strip()}" for line in ev.verdict_lines)

    return f"""## {case.name} — {status}

**{case.description}**

| Field | Value |
|-------|-------|
| User ID | `{case.user_id}` |
| Search query | {case.search_query!r} |
| Expect additive | {case.expect_additive} |
| Memories stored | {ev.total_stored} |
| Search hits | {ev.search_hit_count} |
| {case.stale_label} in search | {ev.stale_returned} |
| {case.current_label} in search | {ev.current_returned} |
| Step 1 `add()` events | {", ".join(initial_events)} |
| Step 2 `add()` events | {", ".join(update_events)} |

### Markers in search

{_format_markers(ev)}

### Verdict

{verdict}

<details>
<summary>Raw Step 1 — initial add()</summary>

```json
{json.dumps(run.scenario.add_initial, indent=2, default=str)}
```

</details>

<details>
<summary>Raw Step 2 — update add()</summary>

```json
{json.dumps(run.scenario.add_update, indent=2, default=str)}
```

</details>

<details>
<summary>Raw Step 3 — search results</summary>

```json
{json.dumps(run.scenario.search_results, indent=2, default=str)}
```

</details>

<details>
<summary>Raw Step 4 — all stored memories</summary>

```json
{json.dumps(run.scenario.all_memories, indent=2, default=str)}
```

</details>

"""


def suite_to_markdown(suite: SuiteRun) -> str:
    run_at = suite.run_at.strftime("%Y-%m-%d %H:%M:%S UTC") if suite.run_at else "—"
    summary_rows = "\n".join(
        f"| `{run.scenario.case.name}` | {_status(run.evaluation.passed)} |"
        for run in suite.cases
    )
    case_sections = "\n".join(_format_case_section(run) for run in suite.cases)

    return f"""# Firecast Test Results

**Run at:** {run_at}  
**Score:** {suite.passed_count} / {suite.total_count} passed

## Suite summary

| Case | Result |
|------|--------|
{summary_rows}

---

{case_sections}
"""


def write_results(suite: SuiteRun, output_stem: Path | str | None = None) -> tuple[Path, Path]:
    """Write JSON and Markdown result files. Returns (json_path, md_path)."""
    stem = Path(output_stem) if output_stem else DEFAULT_OUTPUT_STEM
    if stem.suffix:
        stem = stem.with_suffix("")
    stem.parent.mkdir(parents=True, exist_ok=True)

    json_path = stem.with_suffix(".json")
    md_path = stem.with_suffix(".md")

    payload = suite_to_dict(suite)
    json_path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    md_path.write_text(suite_to_markdown(suite))

    return json_path, md_path
