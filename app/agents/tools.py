from ..config import TAVILY_API_KEY, logger
from tavily import AsyncTavilyClient

# Tool: Web search
async def search_web(query: str) -> str:
    logger.info(f"Web search triggered for query: {query}")
    client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
    return str(await client.search(query))
