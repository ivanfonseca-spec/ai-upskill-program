# Quick test
import sys
from pathlib import Path

# Allow running this script directly (adds project root to sys.path)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage


async def test_github():
    transformer = ArticleTransformer()
    storage = MarkdownStorage()

    fetcher = GitHubTrendingFetcher(transformer, storage)
    articles = await fetcher.fetch_and_save()

    print(f"✅ Fetched {len(articles)} trending repos!")
    print(f"First: {articles[0].title}")


# Run it
import asyncio
asyncio.run(test_github())
