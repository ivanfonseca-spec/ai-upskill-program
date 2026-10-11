# test_workflow.py
import sys
import asyncio
from pathlib import Path

# Allow running this script directly (adds project root to sys.path)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage


async def main():
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/articles")

    fetcher = HackerNewsFetcher(transformer, storage)
    articles = await fetcher.fetch_and_save()
    print(f"✅ Done! Fetched and saved {len(articles)} articles")


asyncio.run(main())
