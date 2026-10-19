# AI Upskill Project

**Multi-agent news aggregation system with MCP integration**

A production-ready AI agent pipeline that fetches, filters, summarizes, and writes AI/ML news newsletters.

## Features

- 🚀 **Async News Fetching** from multiple sources (HackerNews, RSS, GitHub Trending)
- 🤖 **AI-Powered Filtering** via LiteLLM (default: Claude Haiku 4.5; swap providers via env var)
- 🔧 **MCP Integration** with a reusable database server and client tools
- 📝 **Multi-Agent Pipeline** (Filter → Summarize → Write)
- 💾 **SQLite Database** for article storage
- 📊 **Evaluation Framework** for quality measurement (accuracy, precision, recall, F1)
- ✅ **60%+ Test Coverage**

## Quick Start

### Prerequisites

- Python 3.11+
- One LLM provider API key (Anthropic recommended; OpenAI, Gemini, or any other [LiteLLM-supported provider](https://docs.litellm.ai/docs/providers) also works)

### Installation

```bash
# Clone repo
git clone https://github.com/BLEND360/AIUpskillProject.git
cd AIUpskillProject

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your provider API key
```

### Run Complete Pipeline

```bash
# Fetch -> Database -> Filter -> Summarize -> Write, end to end
python -m src.complete_pipeline

# Output:
# - data/output/newsletter.md       (final newsletter)
# - data/context/                   (intermediate agent outputs)
# - data/news_agent.db              (article database)
```

### Run Individual Components

```bash
# Fetch articles only
python -m src.main

# Fetch + filter (no summarize/write)
python -m src.pipeline

# Evaluate filtering quality against the golden dataset
python src/evaluation/evaluator.py
```

## Architecture

```
┌──────────────────────────────────────────────┐
│              News Sources                      │
│   HackerNews  |  RSS Feeds  |  GitHub Trending │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │  FetchOrchestrator   │
            │    (Milestone 1)     │
            └──────────┬───────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  SQLite Database  │  ← queried via MCP
              │ (DatabaseManager) │     (database_server.py)
              └──────────┬─────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │   NewsFilterAgent    │
            │   (LiteLLM + tools)  │
            └──────────┬───────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │   SummarizerAgent    │
            │  (+ SearchSkill/MCP) │
            └──────────┬───────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │     WriterAgent       │
            │ (newsletter copy)    │
            └──────────┬───────────┘
                       │
                       ▼
                📄 newsletter.md
```

## Project Structure

```
AIUpskillProject/
├── src/
│   ├── agents/              # AI agents (Template Method pattern)
│   │   ├── base_agent.py
│   │   ├── news_filter_agent.py
│   │   ├── enhanced_filter_agent.py
│   │   ├── summarizer_agent.py
│   │   └── writer_agent.py
│   ├── fetchers/            # News fetchers (Open/Closed via BaseFetcher)
│   ├── storage/              # Markdown / JSON article storage
│   ├── transformers/         # Article normalization
│   ├── factories/            # FetcherFactory
│   ├── strategies/           # Rate-limiting strategy
│   ├── utils/                # RateLimiter
│   ├── database/             # DatabaseManager (SQLite via aiosqlite)
│   ├── mcp/                  # MCP servers + client
│   │   ├── hello_server.py
│   │   ├── database_server.py
│   │   └── simple_client.py
│   ├── skills/                # SearchSkill (MCP abstraction layer)
│   ├── tools/                 # LLM-callable tools (calculator, web_search)
│   ├── evaluation/            # Evaluator + golden-dataset scoring
│   ├── models/                 # Article dataclass
│   ├── orchestrator.py         # FetchOrchestrator (DI across fetchers)
│   ├── main.py                 # Fetch-only entry point
│   ├── pipeline.py              # Fetch + filter entry point
│   └── complete_pipeline.py     # Full fetch->DB->filter->summarize->write
├── tests/                       # pytest suite
├── scripts/                     # Manual verification scripts
├── data/
│   ├── articles/                 # Raw fetcher output (gitignored)
│   ├── context/                   # Filtered/summarized intermediate output
│   ├── output/                     # Final newsletter
│   └── evaluation/                 # Golden dataset + evaluation report
└── docs/                          # Course documentation + milestones
```

## Key Technologies

- **Python 3.11+** - Core language
- **aiohttp** - Async HTTP requests
- **feedparser** - RSS parsing
- **LiteLLM** - LLM provider abstraction (default: Claude Haiku 4.5)
- **MCP** - Model Context Protocol
- **aiosqlite / SQLite** - Local article database
- **pytest / pytest-asyncio / pytest-cov** - Testing
- **black / ruff** - Formatting and linting

## Milestones Completed

- ✅ Milestone 0: Setup
- ✅ Milestone 1: Async News Fetcher
- ✅ Milestone 2: SOLID Refactoring
- ✅ Milestone 3: First Agent with Tools
- ✅ Milestone 4: MCP-Powered Pipeline
- ✅ Milestone 5: Evaluation & Documentation

See `docs/milestones/` for the original per-milestone instructions.

## Evaluation Metrics

Filtering quality is measured against a 10-case hand-labeled golden dataset (`data/evaluation/golden_dataset.json`). Run the evaluator to generate current numbers:

```bash
python src/evaluation/evaluator.py
cat data/evaluation/evaluation_report.md
```

The report includes accuracy, precision, recall, and F1, plus a per-case breakdown (expected vs. predicted, with the LLM's reasoning). Results vary slightly with the configured model/provider, so the report is regenerated rather than hardcoded here.

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## Development

### Code Style

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/
```

### Adding New Sources

1. Create a fetcher in `src/fetchers/`
2. Inherit from `BaseFetcher`
3. Implement `fetch_articles()` and `get_source_name()`
4. Register it in `FetchOrchestrator` / `src/main.py`

### Adding New MCP Tools

1. Add the tool schema to the relevant MCP server (`src/mcp/`)
2. Implement the tool function
3. Register it in `@server.call_tool()`
4. Test it with an MCP client

## License

MIT

## Acknowledgments

Built as part of Blend's internal AI Upskill program ([Agentic Build Program](https://friedcheesee.github.io/agentic-build-program/)).
