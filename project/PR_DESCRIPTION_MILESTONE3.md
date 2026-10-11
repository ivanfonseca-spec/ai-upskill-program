# Milestone 3: First AI Agent (Tool Use + Filtering)

## Summary

Added an AI agent layer on top of the Milestone 1/2 fetch pipeline: agents read fetched articles, use an LLM (via LiteLLM) to judge AI/ML relevance, and optionally call tools (calculator, web search) while reasoning.

## Changes

### Agents (`src/agents/`)

- `base_agent.py` — `BaseAgent` abstract class. Template Method pattern: `execute()` defines the fixed workflow (load → process → save), subclasses implement `_load_context`, `_process`, `_save_result`. Also provides `_call_llm()` and `_call_llm_with_tools()` (tool-calling loop, capped at 10 rounds to avoid infinite loops).
- `news_filter_agent.py` — `NewsFilterAgent`: parses fetched markdown, asks the LLM to score each article's AI/ML relevance (1-10, threshold 6), saves the filtered set to markdown.
- `enhanced_filter_agent.py` — `EnhancedFilterAgent(NewsFilterAgent)`: same filtering logic, but gives the LLM access to two tools (`calculator`, `web_search`) via `BaseAgent`'s tool-calling loop. Demonstrates DIP/OCP — extends the filter agent without modifying it.

### Tools (`src/tools/`)

- `calculator.py` — evaluates simple math expressions (sandboxed `eval`, no builtins).
- `web_search.py` — mocked web search (returns canned results; real API swap is a drop-in later).

### Pipeline (`src/pipeline.py`)

- `run_pipeline()` wires Milestone 1/2's `FetchOrchestrator` + fetchers + storage together with `NewsFilterAgent`, producing: fetch → filter → save, end to end.

### Supporting changes

- Minor fixes in `fetcher_factory.py`, `github_trending_fetcher.py`, `hackernews_fetcher.py`, `article_transformer.py`, `orchestrator.py`, `rate_limit_strategy.py` to support the pipeline.
- `requirements.txt`: added `black` (formatter).
- Test updates: `test_orchestrator.py`, `test_patterns.py`, `test_substitutability.py`, `test_hackernews_fetcher.py` adjusted for the above; new `tests/test_news_filter_agent.py`.
- Manual verification scripts: `scripts/test_base_agent.py`, `scripts/test_filter_agent.py`, `scripts/test_enhanced_agent.py`, `scripts/test_llm.py`, `scripts/llm_examples.py`.

## Design Principle Focus

Per the Milestone 2 roadmap notes (`docs/design-decisions.md`): **Milestone 3 leans on Dependency Inversion** — agents depend on the `BaseAgent` abstraction (Template Method), and `EnhancedFilterAgent` extends `NewsFilterAgent` via inheritance + tool injection rather than modifying it (OCP).

## Known gap / to verify

`pipeline.py` points the filter agent at `data/articles/all_articles.md`, but neither `FetchOrchestrator` nor any fetcher currently writes a combined `all_articles.md` — each fetcher saves its own `<source>_articles.md` (a gap flagged back in Milestone 2). A file with that name exists in the repo, but it looks hand-assembled rather than pipeline-generated. Worth confirming `run_pipeline()` actually runs clean end-to-end before merging, or wiring a combined-file step into the orchestrator/storage.

## Testing

- [ ] Run `pytest tests/ -v` with venv activated and confirm pass/fail counts (not yet re-verified after this milestone's changes)
- [ ] Run `python -m src.pipeline` end-to-end and confirm it doesn't hit the gap above

## Files Changed

**Added:**
- src/agents/base_agent.py
- src/agents/news_filter_agent.py
- src/agents/enhanced_filter_agent.py
- src/tools/calculator.py
- src/tools/web_search.py
- src/pipeline.py
- tests/test_news_filter_agent.py
- scripts/test_base_agent.py, scripts/test_filter_agent.py, scripts/test_enhanced_agent.py, scripts/test_llm.py, scripts/llm_examples.py

**Modified:**
- src/factories/fetcher_factory.py
- src/fetchers/github_trending_fetcher.py
- src/fetchers/hackernews_fetcher.py
- src/transformers/article_transformer.py
- src/orchestrator.py
- src/strategies/rate_limit_strategy.py
- src/main.py
- requirements.txt
- tests/test_orchestrator.py, tests/test_patterns.py, tests/test_substitutability.py, tests/test_hackernews_fetcher.py

---

**⚠️ Depends on #28:** Milestone 2 (`feature/milestone-2-solid`) is not yet merged to `main`, and a stacked PR isn't possible here (the base branch for a PR must exist in `BLEND360/AIUpskillProject`, and I don't have push access to create it there — only forks can be used as the head). So this PR's diff includes both Milestone 2's and Milestone 3's commits until #28 merges. **Please review/merge #28 first**; once it's in, this diff will shrink to just the Milestone 3 changes listed above.

**Ready for:** Checkpoint 3 review (pending #28)
