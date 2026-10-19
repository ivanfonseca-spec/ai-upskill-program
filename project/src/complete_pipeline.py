"""Complete multi-agent pipeline with MCP."""

import asyncio
import sys
from pathlib import Path

# Allow running this file directly ("python src/complete_pipeline.py"): Python
# puts the script's own directory (src/) on sys.path[0] instead of the project
# root, so "from src.orchestrator..." below fails with ModuleNotFoundError otherwise.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.orchestrator import FetchOrchestrator
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage
from src.agents.news_filter_agent import NewsFilterAgent
from src.agents.summarizer_agent import SummarizerAgent
from src.agents.writer_agent import WriterAgent
from src.database.db_manager import DatabaseManager


async def run_complete_pipeline():
    """
    Run complete pipeline:
    1. Fetch articles (Milestone 1)
    2. Save to database
    3. Filter with AI (Milestone 3)
    4. Summarize (Milestone 4)
    5. Write newsletter (Milestone 4)
    """
    print("=" * 70)
    print("  Complete AI Agent Pipeline with MCP")
    print("=" * 70)

    # Step 1: Fetch
    print("\n📰 Step 1: Fetching articles from sources...")

    # FetchOrchestrator takes injected dependencies (DI from the Milestone 2
    # SOLID refactor) — same wiring as src/main.py and src/pipeline.py.
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

    # Each fetcher's fetch_and_save() only writes its own "<source>_articles.md"
    # file — nothing produces a combined file, but Step 3 (filtering) needs one.
    # Write it explicitly here.
    fetch_output = Path("data/articles/all_articles.md")
    storage.save(articles, "all_articles.md")
    print(f"✅ Fetched {len(articles)} articles → {fetch_output}")

    # Step 2: Save to database
    print("\n💾 Step 2: Saving to database...")
    db = DatabaseManager()
    await db.initialize()
    for article in articles:
        await db.insert_article(
            {
                "title": article.title,
                "url": article.url,
                "source": article.source,
                "published_at": article.published_at.isoformat(),
                "summary": article.summary,
                "score": article.score,
            }
        )
    db_articles = await db.query_articles(limit=1000)
    print(f"✅ Database has {len(db_articles)} articles")

    # Step 3: Filter
    print("\n🤖 Step 3: Filtering with AI agent...")
    filter_agent = NewsFilterAgent()
    filter_output = Path("data/context/filtered_articles.md")
    await filter_agent.execute(
        input_path=str(fetch_output), output_path=str(filter_output)
    )
    print(f"✅ Filtered articles → {filter_output}")

    # Step 4: Summarize
    print("\n📝 Step 4: Summarizing with AI agent...")
    summarizer = SummarizerAgent()
    summary_output = Path("data/context/summary.md")
    await summarizer.execute(
        input_path=str(filter_output), output_path=str(summary_output)
    )
    print(f"✅ Summary → {summary_output}")

    # Step 5: Write
    print("\n✍️  Step 5: Writing newsletter...")
    writer = WriterAgent()
    newsletter_output = Path("data/output/newsletter.md")
    await writer.execute(
        input_path=str(summary_output), output_path=str(newsletter_output)
    )
    print(f"✅ Newsletter → {newsletter_output}")

    print("\n" + "=" * 70)
    print("🎉 Complete Pipeline Success!")
    print("=" * 70)
    print(f"\n📊 Pipeline Summary:")
    print(f"   1. Fetched: {len(articles)} articles")
    print(f"   2. Database: {len(db_articles)} total articles")
    print(f"   3. Filtered: {filter_output}")
    print(f"   4. Summarized: {summary_output}")
    print(f"   5. Newsletter: {newsletter_output}")
    print(f"\n📖 Read your newsletter:")
    print(f"   cat {newsletter_output}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_complete_pipeline())
