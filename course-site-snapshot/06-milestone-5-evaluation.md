<!-- Snapshot of https://friedcheesee.github.io/agentic-build-program/milestone-5-evaluation/ — fetched 2026-10-10 (condensed; full code listings live in the project itself) -->

# Milestone 5: Evaluation & Documentation

**Time Commitment:** 2-3 evenings (4-6 hours)
**When:** Week 5, Days 23-25
**Prerequisites:** Milestone 4 complete and PR merged
**Checkpoint:** Checkpoint 5 (FINAL)
**Next:** Project Complete!

## Learning Objectives

Create golden evaluation datasets, implement basic evaluation metrics, measure AI agent quality, write comprehensive documentation, complete a production-ready, portfolio-quality project.

## Week 5 Overview

```
Evening 23 (Mon): Golden Dataset + Basic Evaluation
Evening 24 (Tue): Documentation
Evening 25 (Wed): Final PR
```

## Evening 23: Golden Dataset + Evaluation

Create `data/evaluation/golden_dataset.json`: 10 hand-labeled test cases (title, summary, expected_relevant, expected_score, reason), balanced 5 relevant / 5 not, covering edge cases (ML/LLM/generative/ethics topics vs. web dev/DevOps/databases/cooking).

Implement `src/evaluation/evaluator.py` (`FilterEvaluator`): runs `NewsFilterAgent._judge_relevance` against each golden test case, compares predicted vs. expected relevance, computes accuracy / precision / recall / F1, and writes `data/evaluation/evaluation_report.md`.

```bash
python src/evaluation/evaluator.py
cat data/evaluation/evaluation_report.md
```

Expected: accuracy 80-90%, precision 85-95%, recall 75-85%, F1 0.80-0.90. If low: improve prompts, adjust threshold, add more examples.

**Deliverable:** Golden dataset (10 cases), evaluation framework, metrics calculated, evaluation report generated.

## Evening 24: Documentation

Update `README.md`: features, quick start (clone, venv, install, configure `.env`), run complete pipeline / individual components, architecture diagram (Sources → FetchOrchestrator → Database (MCP) → FilterAgent → SummarizerAgent (+SearchSkill) → WriterAgent → Newsletter), project structure, key technologies (Python 3.11+, aiohttp, LiteLLM, MCP, SQLite, pytest, ruff), milestones completed, evaluation metrics, running tests, development notes (code style, adding sources, adding MCP tools).

Write `docs/architecture.md`: design principles (SOLID, Template Method/Factory/Strategy/Observer patterns, async-first), component details per milestone, data flow, technology choices and why, performance notes, security notes (API keys in `.env`, parameterized queries, safe JSON parsing), future enhancements.

Write `docs/deployment.md`: local deployment steps, scheduling (cron / Windows Task Scheduler), optional Docker, configuration (env vars), monitoring, troubleshooting.

**Deliverable:** README updated, architecture documented, deployment guide written.

## Evening 25: Final PR

```bash
pytest tests/ -v
pytest tests/ --cov=src
black src/ tests/
isort src/ tests/
python src/complete_pipeline.py
cat data/evaluation/evaluation_report.md
```

PR summarizes: golden dataset, evaluation framework (accuracy/precision/recall/F1), documentation (README, architecture, deployment guide). Marks the project complete.

## MILESTONE 5 COMPLETE - PROJECT DONE!

**Overall:** Week 1 async fetching → Week 2 SOLID & refactoring → Week 3 AI agents with tool use → Week 4 MCP servers & multi-agent pipeline → Week 5 evaluation & documentation.

**Skill set (130+ skills)** across software engineering, AI engineering, MCP & tools, and production concerns (databases, evaluation, documentation, deployment).

**Final project stats (per curriculum):** ~2000 lines of production code, ~800 lines of tests, 60%+ coverage, 2 fetchers, 4 AI agents, 1 MCP server (3 tools), 1 reusable skill, complete pipeline, full documentation set.

**Checkpoint 5 (FINAL):** 2 reviewers + 1 senior approval. Rubric checks evaluation framework working, metrics reasonable (80%+ accuracy), documentation comprehensive, project production-ready.

**Total time invested:** 38-54 hours over 5 weeks.
