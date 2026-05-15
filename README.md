# Firecast — Mem0 Temporal Reasoning Evaluation

Hands-on test suite for evaluating [Mem0](https://mem0.ai) (open-source memory layer) on **temporal reasoning**: whether newer facts **supersede** older conflicting ones, or are stored and retrieved additively.

## Hypothesis

Base Mem0 (vector search + LLM memory extraction) will **not** reliably detect conflicts between superseding facts. It may merge silently, keep both versions, or return stale data in search results.

The `additive_control` case is a sanity check: non-conflicting facts should coexist.

## Test cases

| Case | Scenario | Expected |
|------|----------|----------|
| `fire_distance` | Wildfire 5 mi → 2 mi | Only current distance in search |
| `location_change` | Austin → Denver | Only current city |
| `budget_update` | $10k → $50k | Only revised budget |
| `allergy_contradiction` | Peanut allergy → cleared | Only current health status |
| `additive_control` | Hiking + coffee | **Both** facts stored and retrievable |

Each case uses a distinct `user_id` to avoid cross-contamination in the vector store.

## Requirements

- Python 3.10+
- OpenAI API key(s) with access to embedding and chat models
- Dependencies: `mem0ai`, `chromadb`, `python-dotenv`

## Setup

```bash
git clone https://github.com/Shubhampreet98/bsv-mem0-testing.git
cd bsv-mem0-testing

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your OPENAI_API_KEY (and optional OPENAI_LLM_API_KEY)
```

Verify OpenAI model access:

```bash
python scripts/check_openai_access.py
```

## Run tests

Full suite (recommended: clean Chroma store first):

```bash
rm -rf .mem0/chroma
python firecast_test.py
```

Single case:

```bash
python firecast_test.py --case fire_distance
```

Custom results path:

```bash
python firecast_test.py --output reports/run1
```

## Output

After each run, results are written to:

- `output/firecast_results.md` — human-readable report
- `output/firecast_results.json` — machine-readable payload

The suite exits with code `1` if any case fails.

## Project layout

```
firecast_test.py          # CLI entry point
firecast/
  cases.py                # Test case definitions
  scenario.py             # add → add → search → get_all
  evaluation.py           # Pass/fail rules
  client.py               # Mem0 + Chroma + OpenAI config
  results_output.py       # JSON/Markdown export
scripts/
  check_openai_access.py  # Pre-flight API check
MEM0_EVALUATION_REPORT.md # Full product evaluation write-up
```

## Configuration

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Embeddings (required) |
| `OPENAI_LLM_API_KEY` | Chat model if on a different OpenAI project |
| `OPENAI_EMBEDDING_MODEL` | Default: `text-embedding-3-small` |
| `OPENAI_LLM_MODEL` | Default: `gpt-4o-mini` |

Mem0 uses **Chroma** locally (`.mem0/chroma`) instead of the default Qdrant backend.

## Documentation

See [MEM0_EVALUATION_REPORT.md](MEM0_EVALUATION_REPORT.md) for hands-on testing notes, technical evaluation, strategic insights, and canonical run results.

## License

Internal evaluation project — adjust license as needed for your organization.
