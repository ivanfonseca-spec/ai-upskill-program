<!-- Snapshot of https://friedcheesee.github.io/agentic-build-program/milestone-1-async-fetcher/ — fetched 2026-10-10 (condensed; full code listings live in the project itself) -->

# Milestone 1: Async News Fetcher

**Time Commitment:** 3-4 evenings (6-8 hours)
**When:** Week 1, Days 2-5
**Prerequisites:** Milestone 0 complete
**Checkpoint:** Checkpoint 1 (after completion)
**Next Milestone:** Milestone 2: SOLID Refactoring

## Learning Objectives

By the end of this week: async/await fundamentals, async HTTP requests with aiohttp, RSS feed parsing, basic rate limiting, saving data to markdown files, async tests with pytest, first production-ready component.

## Week 1 Overview

```
Day 1 (Evening 1): Milestone 0 - Setup
Day 2 (Evening 2): Async Basics + HackerNews Fetcher
Day 3 (Evening 3): RSS Fetcher + Rate Limiting
Day 4 (Evening 4): Orchestrator + Tests
Day 5 (Evening 5): Polish + PR (optional)
```

## Evening 2: Async Basics + HackerNews Fetcher

Understand `async def` / `await` / `asyncio.gather()`. Build `src/models/article.py` (`Article` dataclass: title, url, published_at, source, summary, score). Build `src/fetchers/hackernews_fetcher.py` (`HackerNewsFetcher`, fetches top story IDs then stories concurrently via `asyncio.gather`). Build `src/storage/markdown_storage.py` (`MarkdownStorage`, saves articles to `data/articles/*.md`). Wire `fetch_and_save()` on the fetcher. Write `tests/test_hackernews_fetcher.py` with `@pytest.mark.asyncio`.

**Deliverable:** HackerNews fetcher working, async concurrent fetching, articles saved to markdown, basic tests passing.

## Evening 3: RSS Fetcher + Rate Limiting

Install `feedparser`. Build `src/fetchers/rss_fetcher.py` (`RSSFetcher`, parses feed via `feedparser.parse` run in an executor since feedparser is sync). Build `src/utils/rate_limiter.py` (`RateLimiter`, semaphore-based, `max_concurrent` operations). Wire rate limiting into `HackerNewsFetcher._fetch_story`. Write `tests/test_fetchers_integration.py` (`test_both_fetchers`, `test_concurrent_fetching`).

**Deliverable:** RSS fetcher working, rate limiting implemented, both fetchers tested, concurrent fetching working.

## Evening 4: Orchestrator + Complete Tests

Build `src/orchestrator.py` (`FetchOrchestrator`, coordinates HackerNews + RSS fetchers, `fetch_all()` runs them concurrently via `asyncio.gather(..., return_exceptions=True)`, saves combined `all_articles.md`). Build `src/main.py` entry point. Write comprehensive tests (`tests/test_article.py`, `tests/test_storage.py`, `tests/test_orchestrator.py`). Check coverage target: 60%+.

**Deliverable:** Orchestrator coordinating all fetchers, main entry point working, comprehensive test suite, 60%+ coverage.

## Evening 5: Polish & PR (Optional)

```bash
black src/ tests/
isort src/ tests/
pylint src/
pytest tests/ -v
```

Create PR describing: 2 fetchers (HackerNews, RSS), infrastructure (Article model, markdown storage, rate limiting, orchestrator), full async implementation, performance (~5x faster than sequential), 60%+ test coverage.

```bash
git add .
git commit -m "feat: async news fetcher with HackerNews and RSS support"
git push origin feature/milestone-1-async-fetcher
```

## Milestone 1 Complete!

**Skills gained (12):** async/await fundamentals, aiohttp, RSS parsing, concurrent task execution, rate limiting with Semaphore, error handling in async code, markdown generation, dataclasses, async testing with pytest, coverage measurement, code organization, integration testing.

**Performance:** sequential ~10-15s → async ~2-3s (5x faster).

**Checkpoint 1 reviews for:** async proficiency, code quality, testing (60%+ coverage), functionality (2+ sources, markdown output, rate limiting). Required approvals: 2 reviewers.

**Next:** Milestone 2: SOLID Refactoring (Week 2, 4-5 evenings, 8-10 hours).
