# Deployment Guide

## Local Deployment (Recommended)

This project is designed to run locally. No cloud deployment is required — everything (fetching, the LLM calls via LiteLLM, the SQLite database, the MCP server) runs on your own machine.

### Requirements

- Windows, macOS, or Linux
- Python 3.11+
- ~500MB disk space (mostly the virtual environment)
- One LLM provider API key (see `docs/milestones/milestone-0-setup.md` or the project README)

### Setup

See the main `README.md` for full installation steps (clone, venv, `pip install -r requirements.txt`, `.env` configuration).

### Running

```powershell
# Activate the virtual environment (Windows)
venv\Scripts\activate

# Run the complete pipeline
python -m src.complete_pipeline
# (direct invocation also works: python src/complete_pipeline.py)
```

Output lands in:
- `data/output/newsletter.md` — the final newsletter
- `data/context/filtered_articles.md`, `data/context/summary.md` — intermediate agent outputs
- `data/news_agent.db` — the SQLite article database

### Scheduling

**Windows (Task Scheduler):**

1. Open Task Scheduler → Create Basic Task
2. Trigger: Daily, at whatever time you want the newsletter generated
3. Action: Start a program
   - Program: `C:\Users\Ivan Fonseca\AIUpskillProject\venv\Scripts\python.exe`
   - Arguments: `-m src.complete_pipeline`
   - Start in: `C:\Users\Ivan Fonseca\AIUpskillProject`

**macOS/Linux (cron):**

```bash
crontab -e
# Run daily at 9 AM
0 9 * * * cd /path/to/AIUpskillProject && ./venv/bin/python -m src.complete_pipeline
```

## Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "src.complete_pipeline"]
```

```bash
docker build -t aiupskillproject .
docker run --env-file .env -v $(pwd)/data:/app/data aiupskillproject
```

## Configuration

Environment variables (set in `.env`, copied from `.env.example`):

| Variable | Required | Notes |
|---|---|---|
| `LITELLM_MODEL` | Yes | e.g. `claude-haiku-4-5-20251001`. Determines which provider key is needed. |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GEMINI_API_KEY` | Yes (one) | Must match the provider implied by `LITELLM_MODEL`. |
| `ENVIRONMENT` | No | `development` / `production` — informational only. |
| `LOG_LEVEL` | No | `INFO` / `DEBUG` — informational only; the project currently logs via `print()`, not a logging framework. |

**Never commit `.env`** — it holds a real API key. It's already in `.gitignore`.

## Monitoring

This project doesn't have a separate logging/metrics stack — progress and errors print directly to the console as each pipeline stage runs. To check on a run after the fact:

```bash
# Did the newsletter get generated, and when?
Get-ChildItem data\output\newsletter.md | Select-Object LastWriteTime   # PowerShell
# or: ls -la data/output/newsletter.md                                  # macOS/Linux

# How many articles are in the database?
sqlite3 data/news_agent.db "SELECT COUNT(*) FROM articles;"
sqlite3 data/news_agent.db "SELECT source, COUNT(*) FROM articles GROUP BY source;"

# How is the filter agent performing?
python src/evaluation/evaluator.py
cat data/evaluation/evaluation_report.md
```

## Troubleshooting

**`UnicodeEncodeError` / `UnicodeDecodeError` on Windows** — the project writes a lot of emoji/non-ASCII output (status messages, newsletter content). Every file read/write in this codebase explicitly passes `encoding="utf-8"` to avoid Windows' default `cp1252` locale encoding; if you add a new file read/write, do the same. If you see mangled characters (`â€"`, `ðŸ¤–`) when *viewing* a file in PowerShell, that's just the terminal misreading valid UTF-8 — use `Get-Content <file> -Encoding UTF8` instead of `cat`.

**`ModuleNotFoundError: No module named 'src'`** — happens if a script under `src/` is run directly and doesn't have the `sys.path.insert(...)` fix at the top (see any file under `src/mcp/`, `src/evaluation/`, or `src/pipeline.py` for the pattern). All current entry points already handle this; apply the same pattern to any new one.

**`StdioServerParameters` can't find `mcp`** — pass `command=sys.executable` rather than a bare `"python"` string when spawning an MCP server subprocess; a bare `"python"` can resolve to a different interpreter than the active venv.

**LLM / API errors** — check `.env` has the right key for whatever `LITELLM_MODEL` is set to, verify your provider account has remaining credit/quota, and check your internet connection.

**API rate limits** — reduce the number of articles fetched per source, or add delay between LLM calls in the filter agent if you're hitting provider rate limits on a large batch.
