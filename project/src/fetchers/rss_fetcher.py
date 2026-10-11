# src/fetchers/rss_fetcher.py

from src.fetchers.base_fetcher import BaseFetcher
from src.strategies.rate_limit_strategy import SemaphoreStrategy
import feedparser
from typing import List
from src.models.article import Article


class RSSFetcher(BaseFetcher):
    """Fetch from RSS feed."""

    def __init__(self, feed_url: str, transformer, storage, rate_limiter=None):
        super().__init__(transformer, storage)
        self.feed_url = feed_url
        # Use provided strategy or default
        self.rate_limiter = rate_limiter or SemaphoreStrategy(10)

    async def fetch_articles(self) -> List[Article]:
        """Fetch from RSS feed."""
        await self.rate_limiter.acquire()
        try:
            feed = feedparser.parse(self.feed_url)
            return self.transformer.transform_rss(feed.entries)
        except Exception as e:
            print(f"⚠️  RSS fetch failed for {self.feed_url}: {e}")
            return []
        finally:
            self.rate_limiter.release()

    def get_source_name(self) -> str:
        """Return source name."""
        return "rss"
