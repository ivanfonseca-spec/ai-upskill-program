"""JSON implementation of ArticleStorage."""

import json
from pathlib import Path
from typing import List
from datetime import datetime
from src.models.article import Article
from src.storage.base_storage import ArticleStorage


class JSONStorage(ArticleStorage):
    """
    Save articles as JSON.

    Alternate implementation of ArticleStorage. Fetchers and the
    orchestrator only depend on the ArticleStorage interface, so this
    can be swapped in for MarkdownStorage without changing any of them
    (Dependency Inversion / Liskov Substitution in action).
    """

    def __init__(self, base_path: str = "data/articles_json"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, articles: List[Article], filename: str = None) -> Path:
        """
        Save articles to a JSON file.

        Args:
            articles: List of articles to save
            filename: Optional filename, defaults to dated file

        Returns:
            Path to saved file
        """
        if filename is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"articles_{date_str}.json"
        elif filename.endswith(".md"):
            # Fetchers hardcode "<source>_articles.md" - keep the same
            # base name but use the right extension for this backend.
            filename = filename[:-3] + ".json"

        filepath = self.base_path / filename

        data = [
            {
                "title": article.title,
                "url": article.url,
                "published_at": article.published_at.isoformat(),
                "source": article.source,
                "summary": article.summary,
                "score": getattr(article, "score", 0),
            }
            for article in articles
        ]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filepath
