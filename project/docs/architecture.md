# Architecture Documentation

## System Overview

Multi-agent AI system for news aggregation and newsletter generation. Fetches articles from multiple sources, filters them for AI/ML relevance using an LLM, summarizes the result by topic, and writes a finished newsletter — all running locally, with intermediate state passed between stages as markdown files and a SQLite database.

## Design Principles

1. **SOLID Principles**
   - Single Responsibility: each fetcher, storage backend, and agent has one job.
   - Open/Closed: `GitHubTrendingFetcher` was added with zero changes to existing fetchers or the orchestrator — new sources plug in by implementing `BaseFetcher`.
   - Dependency Inversion: `FetchOrchestrator` depends on the `BaseFetcher`/`ArticleStorage` abstractions, with concrete fetchers, storage, and the transformer injected via its constructor (see `src/main.py`, `src/pipeline.py`, `src/complete_pipeline.py`).

2. **Design Patterns**
   - Template Method: `BaseAgent.execute()` fixes the load → process → save lifecycle; `NewsFilterAgent`, `SummarizerAgent`, and `WriterAgent` each implement the three steps.
   - Factory: `FetcherFactory` (`src/factories/`).
   - Strategy: rate limiting (`src/strategies/rate_limit_strategy.py`, `src/utils/rate_limiter.py`) is a swappable semaphore-based strategy.
   - Skill abstraction: `SearchSkill` wraps the database MCP server's `search_articles` tool behind a simple `search(query, limit)` call, so agents don't need to know about MCP plumbing directly.

3. **Async-First**
   - All I/O (HTTP fetches, file reads/writes, database access, MCP calls) is async.
   - `FetchOrchestrator.fetch_all()` runs all fetchers concurrently via `asyncio.gather(..., return_exceptions=True)`, so one failing source doesn't take down the others.

## Component Details

### 1. Fetchers (Milestone 1)

**Purpose:** fetch articles from external sources and save them as markdown.

**Sources:**
- HackerNews API (`src/fetchers/hackernews_fetcher.py`)
- RSS feeds (`src/fetchers/rss_fetcher.py`)
- GitHub Trending (`src/fetchers/github_trending_fetcher.py`) — added later as the Open/Closed proof point

**Key features:** concurrent fetching via `asyncio.gather`, semaphore-based rate limiting, per-source markdown output (`<source>_articles.md`), graceful per-item error handling.

### 2. Agents (Milestones 3-4)

**BaseAgent** (`src/agents/base_agent.py`): Template Method pattern. `execute(input_path, output_path)` always runs `_load_context` → `_process` → `_save_result`. Also provides `_call_llm()` (plain completion) and `_call_llm_with_tools()` (function-calling loop, used by `EnhancedFilterAgent`), both via LiteLLM so the model/provider is swappable through `LITELLM_MODEL`.

**NewsFilterAgent:** reads fetched articles from markdown, asks the LLM to judge AI/ML relevance (returns `relevant`, `relevance_score`, `reasoning`, `key_topics` as JSON), keeps articles scoring at or above the relevance threshold.

**EnhancedFilterAgent:** extends `NewsFilterAgent` with tool use (`calculator`, `web_search`) via the function-calling loop in `BaseAgent`.

**SummarizerAgent:** groups filtered articles by topic and asks the LLM for a short per-topic summary. Holds a `SearchSkill` instance for optional additional context via MCP.

**WriterAgent:** turns the topic summaries into a finished newsletter (intro, per-topic sections, conclusion).

### 3. MCP Integration (Milestone 4)

**Database MCP Server** (`src/mcp/database_server.py`): exposes three tools — `query_articles`, `search_articles`, `get_sources` — backed by `DatabaseManager` (SQLite via `aiosqlite`). Runs over stdio transport, so any MCP-compatible client (including Claude Desktop) could attach to it directly.

**SearchSkill** (`src/skills/search_skill.py`): a reusable, higher-level client that connects to the database MCP server and calls `search_articles`. Demonstrates the "skill" pattern: application code calls `SearchSkill.search(query)` without knowing it's talking to an MCP server underneath.

### 4. Pipeline Orchestration

**Flow:**

```
┌─────────────────────────────────────────────┐
│         News Sources                         │
│  HackerNews | RSS Feeds | GitHub Trending   │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
        ┌──────────────────┐
        │ Fetch Orchestrator│
        │   (Milestone 1)   │
        └──────────┬────────┘
                   │
                   ▼
            ┌──────────┐
            │ Database │ ← MCP Server
            │ (SQLite) │
            └──────────┘
                   │
                   ▼
        ┌──────────────────┐
        │  FilterAgent      │
        │   (LLM + Tools)   │
        └──────────┬────────┘
                   │
                   ▼
        ┌──────────────────┐
        │ SummarizerAgent   │
        │  (+ SearchSkill)  │
        └──────────┬────────┘
                   │
                   ▼
        ┌──────────────────┐
        │  WriterAgent      │
        │   (Newsletter)    │
        └──────────┬────────┘
                   │
                   ▼
           📄 Newsletter.md
```

`src/complete_pipeline.py` wires all five stages together end to end. `src/pipeline.py` and `src/main.py` expose the fetch-only and fetch+filter stages individually, for running or testing a slice of the system without the LLM-heavy summarize/write steps.

**Error handling:** each fetcher failure is isolated (`return_exceptions=True`); LLM JSON-parsing failures in the filter agent fall back to "not relevant" rather than crashing the run.

### 5. Evaluation (Milestone 5)

**Golden dataset** (`data/evaluation/golden_dataset.json`): 10 hand-labeled examples, balanced between AI/ML-relevant and not, covering edge cases (DevOps/database/cooking articles as clear negatives; LLM/generative/ethics articles as clear positives).

**Evaluator** (`src/evaluation/evaluator.py`): runs `NewsFilterAgent._judge_relevance()` against each golden example and computes:
- **Accuracy** — overall correctness.
- **Precision** — of articles predicted relevant, how many actually were (false-positive rate).
- **Recall** — of articles that were actually relevant, how many were found (false-negative rate).
- **F1** — harmonic mean of precision and recall.

Results are written to `data/evaluation/evaluation_report.md` and are regenerated by re-running the evaluator rather than hardcoded, since they shift slightly with the configured model/provider.

## Data Flow

```
External APIs
     ↓
Fetchers (async)
     ↓
Markdown files + SQLite database
     ↓
NewsFilterAgent (LLM via LiteLLM)
     ↓
Filtered markdown
     ↓
SummarizerAgent (LLM + SearchSkill/MCP)
     ↓
Summary markdown
     ↓
WriterAgent (LLM)
     ↓
Newsletter markdown
```

## Technology Choices

**Why Python?** Excellent async support, rich AI/ML ecosystem, easy to read and maintain.

**Why LiteLLM + Claude Haiku 4.5?** LiteLLM lets the project swap LLM providers via an env var with no code changes. Claude Haiku is inexpensive for a project this size, Anthropic's trial credit covers the whole curriculum, and it has solid function-calling and JSON-output support.

**Why SQLite?** No server to run, perfect for local development, trivial to inspect or reset.

**Why MCP?** An emerging standard for exposing tools to LLM-based systems; building a real MCP server (rather than just calling functions directly) demonstrates the protocol and keeps the database access reusable by any MCP client.

**Why Markdown as the hand-off format between stages?** Human-readable, git-friendly, and easy to debug — you can open `data/context/filtered_articles.md` directly and see exactly what the filter agent decided, without needing to inspect a database or an in-memory object.

## Performance

**Observed:** fetching ~30-60 articles across 3 sources takes a few seconds (concurrent); filtering scales with the number of articles since each one is a separate LLM call; the full pipeline (fetch → filter → summarize → write) typically completes in a couple of minutes depending on article volume and the configured model's latency.

**Bottlenecks:** LLM API calls (one round-trip per article during filtering) and network I/O during fetching.

**Mitigations already in place:** concurrent fetching via `asyncio.gather`, semaphore-based rate limiting to avoid overwhelming source APIs.

## Security

**API keys:** stored in `.env` (gitignored, never committed), loaded via `python-dotenv` at runtime, never logged.

**Input handling:** database queries use parameterized SQL (`aiosqlite` placeholders) to avoid injection; LLM JSON output is parsed defensively (fenced-code-block stripping, try/except with a safe fallback) rather than `eval`'d.

**Rate limiting:** semaphore-based, configurable, prevents hammering source APIs.

## Future Enhancements

1. **More sources** — Twitter/X, Reddit, arXiv.
2. **Broader evaluation** — a larger golden dataset, and tracking metrics over time as prompts/models change.
3. **Scheduling** — a cron/Task Scheduler entry to run the pipeline daily (see `docs/deployment.md`).
4. **Richer MCP surface** — additional tools on the database server (e.g. trend/topic aggregation), and a second MCP server if a future source needs its own stateful backend.
