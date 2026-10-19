"""Complete pipeline: Fetch -> Filter."""

import asyncio
import sys
from pathlib import Path

# Allow running this file directly ("python src/pipeline.py"): Python puts the
# script's own directory (src/) on sys.path[0] instead of the project root,
# so "from src.orchestrator..." below fails with ModuleNotFoundError otherwise.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.orchestrator import FetchOrchestrator
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage
from src.agents.news_filter_agent import NewsFilterAgent


async def run_pipeline():
    """
    Run complete pipeline.

    1. Fetch articles (Milestone 1)
    2. Filter with AI agent (Milestone 3)
    """
    print("=" * 60)
    print("  Complete Pipeline: Fetch + Filter")
    print("=" * 60)

    # Step 1: Fetch articles
    print("\n📰 Step 1: Fetching articles...")

    # Same dependency wiring as src/main.py (DI from Milestone 2)
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/articles")
    fetchers = [
        HackerNewsFetcher(transformer, storage),
        RSSFetcher("https://hnrss.org/frontpage", transformer, storage),
        GitHubTrendingFetcher(transformer, storage),
    ]

    orchestrator = FetchOrchestrator(
        fetchers=fetchers,
        storage=storage,
        transformer=transformer,
    )
    articles = await orchestrator.fetch_all()

    fetch_output = Path("data/articles/all_articles.md")
    print(f"✅ Fetched {len(articles)} articles")
    print(f"   Saved to: {fetch_output}")

    # Step 2: Filter with AI
    print("\n🤖 Step 2: Filtering with AI...")
    agent = NewsFilterAgent()
    filter_output = Path("data/context/filtered_articles.md")

    result = await agent.execute(
        input_path=str(fetch_output), output_path=str(filter_output)
    )

    print(f"✅ Filtering complete")
    print(f"   Filtered articles: {filter_output}")

    print("\n" + "=" * 60)
    print("🎉 Pipeline complete!")
    print(f"   1. Fetched: {fetch_output}")
    print(f"   2. Filtered: {filter_output}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_pipeline())
