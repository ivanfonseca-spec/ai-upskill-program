# tests/test_article_transformer.py
from src.transformers.article_transformer import ArticleTransformer


def test_transform_hackernews():
    """Test transforming raw HackerNews data to Articles."""
    transformer = ArticleTransformer()
    raw_hn = [{"title": "Test", "url": "http://example.com", "time": 1234567890}]

    articles = transformer.transform_hackernews(raw_hn)

    assert len(articles) == 1
    assert articles[0].title == "Test"
    assert articles[0].url == "http://example.com"
    assert articles[0].source == "hackernews"


def test_transform_hackernews_skips_missing_url():
    """Items without a URL (Ask HN, etc.) should be skipped."""
    transformer = ArticleTransformer()
    raw_hn = [{"title": "Ask HN: something", "time": 1234567890}]

    articles = transformer.transform_hackernews(raw_hn)

    assert len(articles) == 0
