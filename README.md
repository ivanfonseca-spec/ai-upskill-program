# AI Upskill Program — Portfolio

This repo packages up everything from Blend's **Agentic Build Program** (the "AI Upskill" course): the working project I built, the course documentation I was given, and a snapshot of the course website itself.

Course site: https://friedcheesee.github.io/agentic-build-program/

## What's in here

- **`project/`** — the full codebase built across all milestones: async multi-source news fetcher, SOLID refactor, a first LLM agent with tool use, an MCP (Model Context Protocol) server + multi-agent pipeline (Filter → Summarize → Write), and the project's own copy of the course documentation under `project/docs/`.
- **`course-site-snapshot/`** — a point-in-time snapshot of the course's published pages (home + all 6 milestones), saved as markdown in case the live site changes or moves.

## Milestones

| # | Milestone | What it covers |
|---|-----------|-----------------|
| 0 | Setup | Local dev environment, venv, LLM API key, architecture overview |
| 1 | Async News Fetcher | `async`/`await`, aiohttp, RSS parsing, rate limiting, orchestrator |
| 2 | SOLID Refactoring | SOLID principles, Factory/Strategy/Template Method patterns |
| 3 | First Agent with Tools | LiteLLM integration, prompt engineering, function calling |
| 4 | MCP-Powered Multi-Agent Pipeline | MCP server/client, SQLite, SearchSkill, Summarizer/Writer agents |
| 5 | Evaluation & Documentation | Golden dataset, precision/recall/F1 evaluation, docs |

See `project/docs/milestones/` for the original per-milestone instructions as given, and `course-site-snapshot/` for the same content as published on the course site.

## Running the project

```bash
cd project
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # add your LLM provider API key
python src/complete_pipeline.py
```

See `project/README.md` for full details.

## Origin

Built as part of Blend's internal AI Upskill program, working through the course's milestone-by-milestone curriculum. The original course submission lives at [BLEND360/AIUpskillProject](https://github.com/BLEND360/AIUpskillProject) (via a private fork); this repo is a personal copy for my own portfolio.
