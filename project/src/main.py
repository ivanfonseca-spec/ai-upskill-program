# src/main.py

import sys
from pathlib import Path

# Allow running this file directly ("python src/main.py"): Python puts the
# script's own directory (src/) on sys.path[0] instead of the project root,
# so "from src.orchestrator..." below fails with ModuleNotFoundError otherwise.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.orchestrator import FetchOrchestrator
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage


async def main():
    """Main entry point with dependency injection."""

    # Create dependencies
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/articles")

    # Create fetchers
    fetchers = [
        HackerNewsFetcher(transformer, storage),
        RSSFetcher("https://hnrss.org/frontpage", transformer, storage),
        GitHubTrendingFetcher(transformer, storage),
    ]

    # Inject dependencies into orchestrator
    orchestrator = FetchOrchestrator(
        fetchers=fetchers, storage=storage, transformer=transformer
    )

    # Run
    try:
        articles = await orchestrator.fetch_all()
        print(f"✅ Fetched {len(articles)} articles total")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import asyncio

    exit_code = asyncio.run(main())
    sys.exit(exit_code)
