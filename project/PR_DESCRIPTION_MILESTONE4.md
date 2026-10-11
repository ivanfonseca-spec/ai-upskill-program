## Milestone 4: MCP-Powered Multi-Agent Pipeline

Builds on Milestone 3's agent framework by adding an MCP (Model Context Protocol) server for the article database, a reusable `SearchSkill`, and two new agents (`SummarizerAgent`, `WriterAgent`) that complete a 3-agent pipeline: **Filter → Summarize → Write**.

### What's new

- `src/mcp/hello_server.py`, `src/mcp/simple_client.py` — MCP basics (tool discovery + invocation over stdio).
- `src/database/db_manager.py` — `DatabaseManager`, async SQLite (via `aiosqlite`) for persisting articles.
- `src/mcp/database_server.py` — MCP server exposing `query_articles`, `search_articles`, `get_sources` tools backed by the database.
- `src/skills/search_skill.py` — `SearchSkill`, a reusable abstraction over the MCP `search_articles` tool.
- `src/agents/summarizer_agent.py` — groups filtered articles by topic and summarizes each group via LLM.
- `src/agents/writer_agent.py` — turns the topic summaries into a newsletter.
- `src/complete_pipeline.py` — end-to-end pipeline: fetch → save to DB → filter → summarize → write.
- `scripts/populate_db.py`, `scripts/test_db_server.py`, `scripts/test_summarizer.py` — manual verification scripts.

### Known gaps / to verify

- **No formal pytest suite for this milestone's new code.** Everything above was verified manually (ran each script/server against real data and confirmed output), not via automated tests in `tests/`. `pytest tests/ -v` in this PR only re-runs Milestone 1–3 tests; it does not cover the MCP server, `SearchSkill`, `SummarizerAgent`, `WriterAgent`, or `complete_pipeline.py`.
- `src/pipeline.py` (from Milestone 3) still references `data/articles/all_articles.md`, which no fetcher/orchestrator code generates on its own — each fetcher only writes its own `<source>_articles.md`. This was flagged in PR #29 and remains unresolved there. `src/complete_pipeline.py` in this PR works around it by explicitly calling `storage.save(articles, "all_articles.md")` after fetching, but `pipeline.py` itself was left as-is (out of scope for this milestone, carried over as a pending item).
- `SearchSkill` is instantiated in `SummarizerAgent.__init__` but not yet called anywhere — wired up as a capability per the course material, not yet used in the summarization logic.

### Windows-specific fixes applied

Several Windows-only bugs surfaced building the MCP stdio servers/clients and are fixed throughout this PR's new files:
- `StdioServerParameters(command=...)` uses `sys.executable` instead of a bare `"python"` (which can resolve to a different interpreter than the active venv).
- Every MCP server reconfigures `stdout`/`stdin` (and `stderr` where used) to UTF-8 on Windows, since the default console codepage (cp1252) can't encode emoji/non-ASCII tool output and silently hangs the client.
- Any `print()` reachable from inside an MCP server process goes to `stderr`, since stdout is reserved for the JSON-RPC protocol stream.
- Scripts launched via a relative path explicitly prepend the project root to `sys.path` (Python only adds the script's own directory, not the project root or cwd).
- All text file reads/writes specify `encoding="utf-8"` explicitly, since Windows' default locale encoding (cp1252) can't round-trip the UTF-8 content this project writes.

### Note for reviewers

As with PR #29, this PR targets `main` directly rather than stacking on an unmerged branch, since a stacked PR isn't possible against a repo this account can't push branches to directly. Depends on PR #28 and PR #29 merging first.
