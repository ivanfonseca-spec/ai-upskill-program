# test_filter_agent.py
import sys
from pathlib import Path

# Allow running this script directly (adds project root to sys.path)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from src.agents.news_filter_agent import NewsFilterAgent


async def test_filter():
    """Test filtering agent."""
    agent = NewsFilterAgent()

    # Use articles from Milestone 1
    result = await agent.execute(
        input_path="data/articles/all_articles.md",
        output_path="data/context/filtered_articles.md"
    )

    print(f"\n✅ Filtering complete!")
    print(f"   Input: {result['input_path']}")
    print(f"   Output: {result['output_path']}")


if __name__ == "__main__":
    asyncio.run(test_filter())
