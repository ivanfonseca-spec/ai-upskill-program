<!-- Snapshot of https://friedcheesee.github.io/agentic-build-program/milestone-3-first-agent/ — fetched 2026-10-10 (condensed; full code listings live in the project itself) -->

# Milestone 3: First Agent with Tools

**Time Commitment:** 4-5 evenings (8-10 hours)
**When:** Week 3, Days 11-15
**Prerequisites:** Milestone 2 complete and PR merged
**Checkpoint:** Checkpoint 3
**Next Milestone:** Milestone 4: MCP-Powered Pipeline

## Learning Objectives

AI agent architecture, LiteLLM integration (provider-agnostic LLM client), prompt engineering, function calling / tool use, building `NewsFilterAgent`, graceful LLM error handling, testing AI agent behavior.

## Week 3 Overview

```
Evening 11 (Mon): LiteLLM Setup + Agent Architecture
Evening 12 (Tue): NewsFilterAgent + Prompt Engineering
Evening 13 (Wed): Add Tool Use (Calculator, Search)
Evening 14 (Thu): Test Agent Behavior
Evening 15 (Fri): Integration + PR
```

## Evening 11: LiteLLM Setup + Agent Architecture

LiteLLM smoke test (`litellm.completion(model=..., messages=[...])`). LLM prompting basics (simple completion, JSON output, few-shot learning). Design `src/agents/base_agent.py` (`BaseAgent`, Template Method pattern): `__init__(model=None)` reads `LITELLM_MODEL` from env; `execute(input_path, output_path)` orchestrates `_load_context` → `_process` → `_save_result` (all abstract, implemented by subclasses); `_call_llm(prompt, system=None)` helper wraps `litellm.completion`.

**Deliverable:** LiteLLM smoke test passing, provider key configured, BaseAgent architecture defined (Template Method), ready to build real agents.

## Evening 12: NewsFilterAgent + Prompt Engineering

Design filtering logic: relevant = ML/LLMs/AI research/applications/neural networks/CV/NLP; not relevant = general programming/web dev/DevOps/databases. Output JSON: `{relevant, relevance_score (1-10), reasoning, key_topics}`.

Implement `src/agents/news_filter_agent.py` (`NewsFilterAgent(BaseAgent)`): `_load_context` reads markdown and regex-parses articles (title/URL/summary); `_process` calls `_judge_relevance` per article via LLM, keeps those with `relevant=True` and `relevance_score >= 6`; `_save_result` writes filtered markdown with scores/reasoning/topics.

**Deliverable:** NewsFilterAgent implemented, prompt engineering working, robust JSON parsing, filtering tested, filtered articles saved.

## Evening 13: Add Tool Use

Understand function calling: LiteLLM normalizes to the OpenAI `tools`/`tool_calls` shape across providers. Build `src/tools/calculator.py` (`calculator(expression)` + `CALCULATOR_SCHEMA`) and `src/tools/web_search.py` (`web_search(query, num_results)` mock + `WEB_SEARCH_SCHEMA`). Extend `BaseAgent` with `tools`/`tool_functions`, `register_tool_function`, and `_call_llm_with_tools` (loops up to 10 rounds: send prompt+tools → if `tool_calls` present, execute locally, append assistant + `role: "tool"` messages, call again → return once the model answers with plain text). Build `src/agents/enhanced_filter_agent.py` (`EnhancedFilterAgent(NewsFilterAgent)`) registering both tools and overriding `_judge_relevance` to use `_call_llm_with_tools`.

**Deliverable:** Calculator tool, web search tool (mock), function calling integrated, EnhancedFilterAgent with tools, tool execution tested.

## Evening 14: Testing & Integration

Write `tests/test_news_filter_agent.py` (agent filters correctly from a temp markdown fixture; tool functions callable directly). Build `src/pipeline.py`: fetch (Milestone 1's `FetchOrchestrator`) → filter (`NewsFilterAgent`), end to end.

**Deliverable:** Agent tests written, tool tests passing, end-to-end pipeline working, integration tested.

## Evening 15: Polish & PR

```bash
black src/ tests/
pytest tests/ -v
git add .
git commit -m "feat: AI agent with tool use and filtering"
git push origin feature/milestone-3-agent
```

PR describes: NewsFilterAgent (LLM-judged relevance via LiteLLM), tool use (calculator + mock web search, function calling), BaseAgent architecture (Template Method, reusable, tool registration).

## Milestone 3 Complete!

**Skills gained (15):** LiteLLM setup, provider-agnostic LLM integration, prompt engineering, few-shot learning, JSON output formatting, function calling / tool use, tool schema design, Template Method agent architecture, LLM error handling, async agent execution, context load/save, agent testing, tool registration, integration patterns, pipeline orchestration.

**Checkpoint 3:** 2 reviewer approvals required.

**Next:** Milestone 4: MCP-Powered Pipeline (Week 4, 5-7 evenings, 10-14 hours) — build MCP servers and a multi-agent pipeline.
