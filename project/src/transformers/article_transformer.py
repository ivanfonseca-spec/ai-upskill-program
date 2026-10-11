"""Transform raw data to Article objects."""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from dateutil import parser as date_parser
from src.models.article import Article


class ArticleTransformer:
    """
    Transforms raw data from various sources to Article objects.

    Single Responsibility: Data transformation only.
    """

    def transform_hackernews(self, raw_data: List[Dict]) -> List[Article]:
        """
        Transform HackerNews API response to Articles.

        Args:
            raw_data: List of HN items from API

        Returns:
            List of Article objects
        """
        articles = []

        for item in raw_data:
            # Skip if no URL (Ask HN, etc.) - matches HackerNewsFetcher._fetch_story
            if not item.get("url"):
                continue

            article = Article(
                title=item.get("title", "No Title"),
                url=item["url"],
                published_at=datetime.fromtimestamp(item.get("time", 0)),
                source="hackernews",
                summary=item.get("text", "")[:200],
                score=item.get("score", 0),
            )
            articles.append(article)

        return articles

    def transform_rss(self, entries: List[Any]) -> List[Article]:
        """
        Transform RSS feed entries to Articles.

        Args:
            entries: List of RSS entries from feedparser

        Returns:
            List of Article objects
        """
        articles = []

        for entry in entries:
            # Skip if no URL - matches RSSFetcher._parse_entry
            url = entry.get("link", "")
            if not url:
                continue

            # published falls back to updated, matching RSSFetcher._parse_entry
            published_str = entry.get("published", entry.get("updated", ""))

            # summary falls back to description, then strips HTML tags
            summary = entry.get("summary", entry.get("description", ""))
            summary = re.sub("<.*?>", "", summary)[:200]

            article = Article(
                title=entry.get("title", "No Title"),
                url=url,
                published_at=self._parse_date(published_str),
                source="rss",
                summary=summary,
            )
            articles.append(article)

        return articles

    def _parse_date(self, date_str: Optional[str]) -> datetime:
        """Parse various date formats, falling back to now() on failure."""
        if not date_str:
            return datetime.now()
        try:
            return date_parser.parse(date_str)
        except Exception:
            return datetime.now()
