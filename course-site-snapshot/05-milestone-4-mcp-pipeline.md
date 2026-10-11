<!-- Snapshot of https://friedcheesee.github.io/agentic-build-program/milestone-4-mcp-pipeline/ — fetched 2026-10-10 (condensed; full code listings live in the project itself) -->

# Milestone 4: MCP-Powered Multi-Agent Pipeline

**Time Commitment:** 5-7 evenings (10-14 hours)
**When:** Week 4, Days 16-22
**Prerequisites:** Milestone 3 complete and PR merged
**Checkpoint:** Checkpoint 4
**Next Milestone:** Milestone 5: Evaluation & Documentation

## Learning Objectives

Model Context Protocol (MCP), building a production MCP server (Database server), a reusable agent skill (SearchSkill), a 3-agent pipeline (Filter → Summarize → Write), integrating agents with MCP tools, multi-agent orchestration.

## Week 4 Overview

```
Evening 16 (Mon): MCP Protocol Basics
Evening 17 (Tue): Database MCP Server (Part 1)
Evening 18 (Wed): Database MCP Server (Part 2) — SearchSkill
Evening 19 (Thu): SummarizerAgent
Evening 20 (Fri): WriterAgent
Evening 21 (Mon): Complete Pipeline Integration
Evening 22 (Tue): Testing + PR
```

## Evening 16: MCP Protocol Basics

`pip install mcp`. Concepts: Server = tool provider, Client = tool consumer (your agents); communication via stdio (local), HTTP, or WebSocket. Flow: client connects → asks for tool list → calls a tool → gets a result.

Build `src/mcp/hello_server.py` (`Server("hello-world")`, `@server.list_tools()` returns `greet`/`add` `Tool` objects with `inputSchema`, `@server.call_tool()` executes them, `stdio_server()` runs it). Build `src/mcp/simple_client.py` (`StdioServerParameters` + `stdio_client` + `ClientSession`, lists tools then calls `greet`/`add`).

**Deliverable:** MCP SDK installed, hello world server working, client connecting, tool calling functional.

## Evening 17-18: Database MCP Server

Build `src/database/db_manager.py` (`DatabaseManager`, async SQLite via `aiosqlite`; `initialize()` creates the `articles` table + indexes; `insert_article()` with `UNIQUE(url)` dedup; `query_articles(source=None, limit=50)`).

Build `src/mcp/database_server.py`: exposes `query_articles`, `search_articles` (keyword match in title/summary), `get_sources` as MCP tools backed by `DatabaseManager`.

Populate the database from the Milestone 1 markdown files (`populate_db.py`), then test with an MCP client (`test_db_server.py`).

Build `src/skills/search_skill.py` (`SearchSkill`): a reusable, higher-level wrapper that connects to the database MCP server and calls `search_articles` — demonstrates the "skill" pattern (an abstraction layer over raw MCP tools).

**Deliverable:** SQLite database, database MCP server (3 tools), database populated, SearchSkill implemented and tested.

## Evening 19-20: Multi-Agent Pipeline

Build `src/agents/summarizer_agent.py` (`SummarizerAgent(BaseAgent)`): loads filtered articles, groups them by topic, asks the LLM for a 2-3 sentence summary per topic group, saves a digest markdown. Has a `SearchSkill` instance available for additional context (not required to be wired into the summarization logic).

Build `src/agents/writer_agent.py` (`WriterAgent(BaseAgent)`): loads the topic summary, asks the LLM to write an engaging newsletter (intro, topic sections, conclusion), saves it as markdown.

## Evening 21: Complete Pipeline Integration

Build `src/complete_pipeline.py`: fetch (`FetchOrchestrator`) → save to DB (`DatabaseManager`) → filter (`NewsFilterAgent`) → summarize (`SummarizerAgent`) → write (`WriterAgent`), each step printing progress and writing its output file.

## Evening 22: Testing + PR

```bash
pytest tests/ -v
black src/ tests/
git add .
git commit -m "feat: MCP-powered multi-agent pipeline"
git push origin feature/milestone-4-mcp-pipeline
```

## Milestone 4 Complete!

**Skills gained (25):** MCP protocol/server/client implementation, database tools (query/search/sources), skill abstraction pattern, multi-agent orchestration, pipeline design, agent coordination, production integration.

**Next:** Milestone 5: Evaluation & Documentation (Week 5, 2-3 evenings, 4-6 hours).
