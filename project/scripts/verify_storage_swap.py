"""
Verify that storage is swappable (DIP/LSP in action).

Same fetchers, same orchestrator, zero changes to either - only the
storage implementation changes, from MarkdownStorage to JSONStorage.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from src.orchestrator import FetchOrchestrator
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.json_storage import JSONStorage  # <- only this line changes


async def main():
    transformer = ArticleTransformer()

    # Swap: was MarkdownStorage("data/articles"), now JSONStorage.
    storage = JSONStorage("data/articles_json")

    fetchers = [
        HackerNewsFetcher(transformer, storage),
        GitHubTrendingFetcher(transformer, storage),
    ]

    orchestrator = FetchOrchestrator(
        fetchers=fetchers,
        storage=storage,
        transformer=transformer,
    )

    articles = await orchestrator.fetch_all()
    print(f"✅ Fetched {len(articles)} articles, saved as JSON in data/articles_json/")


if __name__ == "__main__":
    asyncio.run(main())
