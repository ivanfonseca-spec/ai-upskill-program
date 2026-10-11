<!-- Snapshot of https://friedcheesee.github.io/agentic-build-program/milestone-0-setup/ — fetched 2026-10-10 -->

# Milestone 0: Local Setup & Architecture

**Time Commitment:** 1 evening (1-2 hours)
**When:** Day 1
**Prerequisites:** None
**Next Milestone:** Milestone 1: Async News Fetcher

## Learning Objectives

By the end of this evening, you will:
- Have a fully configured local development environment
- Understand the project architecture
- Run your first "hello world" test
- Be ready to start coding tomorrow

**This is NOT a coding milestone** - just setup so you can hit the ground running!

## Your Evening Timeline (1-2 hours)

```
7:30 PM - Start
├── 7:30-7:45 PM (15 min) - Clone repo & read README
├── 7:45-8:00 PM (15 min) - Create venv & install dependencies
├── 8:00-8:15 PM (15 min) - Get an LLM API key
├── 8:15-8:25 PM (10 min) - Configure .env file
├── 8:25-8:35 PM (10 min) - Run automated verification
└── 8:35-8:55 PM (20 min) - Read architecture overview
8:55 PM - Done!
```

## Task 1: Clone & Explore (15 minutes)

### Step 1: Clone the repository

```bash
cd ~/projects
git clone https://github.com/BLEND360/AIUpskillProject.git
cd AIUpskillProject
```

### Step 2: Explore the structure

```bash
ls -la
# You should see:
# - src/          # Your code goes here
# - tests/        # Your tests go here
# - docs/         # Documentation and milestones
# - data/         # Output files (created automatically)
# - requirements.txt
# - README.md
# - .env.example
```

### Step 3: Read the README

Read `README.md` for 5 minutes - get the big picture.

## Task 2: Create Virtual Environment (15 minutes)

### Why virtual environments?

Isolates project dependencies from system Python. Essential for clean development.

### Step 1: Create venv

```bash
python3.11 -m venv venv
# macOS/Linux: source venv/bin/activate
# Windows:     venv\Scripts\activate
```

### Step 2: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
# Installs: aiohttp, feedparser, litellm, mcp, pytest/pytest-asyncio/pytest-cov,
# ruff, python-dotenv
```

### Step 4: Verify installation

```bash
python --version
python -c "import aiohttp; import feedparser; print('Core packages installed')"
```

## Task 3: Get an LLM API Key (15 minutes)

The curriculum uses **LiteLLM** as an LLM provider abstraction, so you can pick whichever provider you want — Anthropic, OpenAI, Gemini, or any of the 100+ providers LiteLLM supports. You only need **one** key.

Default: `claude-haiku-4-5-20251001` (Anthropic Claude Haiku 4.5) — cheap (~$1.50 total for the whole curriculum), and Anthropic gives new accounts a $5 trial credit.

**Recommended: Anthropic Claude (5 min)**
1. Go to https://console.anthropic.com/
2. Sign up (free; new accounts get $5 trial credit)
3. Settings → API Keys → Create Key
4. Copy the key (starts with `sk-ant-...`)

**Alternatives:** OpenAI (`gpt-4o-mini`), Google Gemini (`gemini/gemini-2.0-flash`).

## Task 4: Configure Environment (10 minutes)

```bash
cp .env.example .env
```

```
LITELLM_MODEL=claude-haiku-4-5-20251001
ANTHROPIC_API_KEY=sk-ant-your_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

Verify `.env` is ignored: `cat .gitignore | grep .env` — never commit `.env`.

## Task 5: Run Verification (10 minutes)

```bash
python scripts/verify_setup.py
```

Checks: Python version, venv active, dependencies installed, API key configured, directory structure, import paths, LiteLLM reachability.

## Task 6: Read Architecture (20 minutes)

Open `docs/architecture/overview.md`. Focus on: System Overview, Data Flow, Technology Stack, Week-by-week preview.

**Key Concepts:** Everything runs locally (no cloud). Markdown as context (agents communicate via markdown files — human-readable, git-friendly, easy to debug). Progressive complexity (Week 1 async → Week 2 clean code → Week 3 AI agents → Week 4 MCP + multi-agent → Week 5 quality).

## Milestone 0 Complete!

Checklist: venv created & activated, dependencies installed, API keys configured, verification passes, architecture document read.

**Next:** Milestone 1: Async News Fetcher (tomorrow evening) — build a HackerNews fetcher.
