"""
Firecast Temporal Reasoning Test Suite
--------------------------------------
Hypothesis: base Mem0 (vector search + LLM compression) will NOT reliably detect
conflicts between superseding facts (fire distance, location, budget, allergies).
It will merge silently, keep both, or return stale data.

The additive_control case expects both facts to coexist (sanity check).
"""

import argparse
import sys

from firecast.cases import ALL_CASES, CASES_BY_NAME
from firecast.client import create_memory
from firecast.evaluation import evaluate
from firecast.reporting import (
    print_case_header,
    print_evaluation,
    print_scenario_steps,
    print_suite_header,
    print_suite_summary,
)
from firecast.results_output import CaseRun, SuiteRun, write_results
from firecast.scenario import run_scenario


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Firecast temporal reasoning tests")
    parser.add_argument(
        "--case",
        choices=list(CASES_BY_NAME.keys()),
        help="Run a single test case by name",
    )
    parser.add_argument(
        "--output",
        metavar="PATH",
        help="Write results to PATH.json and PATH.md (default: output/firecast_results)",
    )
    parser.add_argument(
        "--no-output-file",
        action="store_true",
        help="Skip writing result files",
    )
    args = parser.parse_args()

    cases = [CASES_BY_NAME[args.case]] if args.case else list(ALL_CASES)

    print_suite_header()
    memory = create_memory()

    summary: list[tuple[str, bool]] = []
    case_runs: list[CaseRun] = []
    for case in cases:
        print_case_header(case)
        scenario_result = run_scenario(memory, case)
        print_scenario_steps(scenario_result)
        evaluation = evaluate(scenario_result)
        print_evaluation(case, evaluation)
        summary.append((case.name, evaluation.passed))
        case_runs.append(CaseRun(scenario=scenario_result, evaluation=evaluation))

    print_suite_summary(summary)

    if not args.no_output_file:
        json_path, md_path = write_results(SuiteRun(cases=case_runs), args.output)
        print(f"\nResults written to:\n  {json_path}\n  {md_path}")

    passed = sum(1 for _, ok in summary if ok)
    if passed < len(summary):
        sys.exit(1)


if __name__ == "__main__":
    main()
