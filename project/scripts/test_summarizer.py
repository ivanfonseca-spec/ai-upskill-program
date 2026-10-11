# test_summarizer.py
import asyncio
import sys
from pathlib import Path

# Allow running this script directly (adds project root to sys.path)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agents.summarizer_agent import SummarizerAgent


async def test():
    agent = SummarizerAgent()
    await agent.execute(
        input_path="data/context/filtered_articles.md",
        output_path="data/context/summary.md"
    )


asyncio.run(test())
