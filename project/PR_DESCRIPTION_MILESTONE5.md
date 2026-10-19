## Milestone 5: Evaluation & Documentation

Final milestone: measures the filtering agent's quality against a hand-labeled dataset and brings the project's documentation up to date.

### What's new

- `data/evaluation/golden_dataset.json` — 10 hand-labeled test cases (balanced relevant/not-relevant, covering edge cases).
- `src/evaluation/evaluator.py` — `FilterEvaluator`: runs `NewsFilterAgent._judge_relevance()` against the golden dataset and computes accuracy, precision, recall, and F1.
- `data/evaluation/evaluation_report.md` — generated report with current results.
- `README.md` — full project overview: features, quick start, architecture diagram, project structure, key technologies, milestones completed, evaluation instructions, running tests, development notes.
- `docs/architecture.md` — design principles (SOLID, patterns used), component-by-component breakdown, data flow, technology choices and why, performance/security notes, future enhancements.
- `docs/deployment.md` — local run instructions, scheduling (Windows Task Scheduler / cron), optional Docker, configuration, monitoring, and a troubleshooting section specific to issues actually hit while building this project (Windows encoding, `sys.path` on direct script invocation, MCP subprocess interpreter resolution).

### Evaluation results

Current run against the golden dataset (see `data/evaluation/evaluation_report.md` for the full per-case breakdown):

- **Accuracy:** 80.0%
- **Precision:** 75.0%
- **Recall:** 100.0%
- **F1 Score:** 0.857
- **Test cases:** 8/10 correct

### Fixes carried in this PR

- Applied the same Windows `sys.path` fix used for `src/mcp/database_server.py` to `src/main.py`, `src/pipeline.py`, and `src/complete_pipeline.py`, so each works whether invoked directly (`python src/pipeline.py`, as the course instructions show) or via `python -m src.pipeline`. This was a real, confirmed bug (`ModuleNotFoundError: No module named 'src'`) hit while verifying this milestone, not just a defensive guess.
- `src/evaluation/evaluator.py` and its file I/O explicitly use `encoding="utf-8"`, consistent with the rest of the codebase (Windows' default locale encoding can't round-trip this project's emoji/non-ASCII output otherwise).

### Known gaps (carried over, not addressed in this PR)

- `src/pipeline.py` still has the `data/articles/all_articles.md` gap flagged in PR #29 (no fetcher writes that combined filename directly — `src/complete_pipeline.py` works around it by calling `storage.save(articles, "all_articles.md")` explicitly, but `pipeline.py` itself was left as-is).
- No pytest-level tests were added for the evaluation framework itself; `evaluator.py` was verified by running it end-to-end and inspecting the generated report.

### Note for reviewers

As with PRs #29 and #30, this targets `main` directly rather than stacking on an unmerged branch (no push access to create intermediate branches upstream). Depends on PRs #28, #29, and #30 merging first.

This completes all 5 milestones of the AI Upskill program.
