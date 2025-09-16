from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
from .config import OPENAI_API_KEY, TAVILY_API_KEY, logger
from tavily import AsyncTavilyClient

# Init LLM
llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Tool: Web search
async def search_web(query: str) -> str:
    logger.info(f"Web search triggered for query: {query}")
    client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
    return str(await client.search(query))

# Agents
research_agent = FunctionAgent(
    name="ResearchAgent",
    description="Specialist in gathering and analyzing information.",
    system_prompt="You are ResearchAgent. Search, analyze, and prepare structured notes.",
    llm=llm,
    tools=[search_web],
)

write_agent = FunctionAgent(
    name="WriteAgent",
    description="Specialist in drafting structured reports.",
    system_prompt="You are WriteAgent. Take research notes and create a clear draft report.",
    llm=llm,
)

review_agent = FunctionAgent(
    name="ReviewAgent",
    description="Specialist in reviewing reports and providing feedback.",
    system_prompt="You are ReviewAgent. Review draft reports, provide improvements, and flag errors.",
    llm=llm,
)

main_agent = FunctionAgent(
    name="MainAgent",
    description="Coordinator agent that delegates to specialized agents.",
    system_prompt=(
        "You are the MainAgent, the coordinator of the workflow. "
        "Your job is to understand the user’s request and decide which specialized agent "
        "to call:\n"
        "- Call ResearchAgent if more research is needed.\n"
        "- Call WriteAgent if a report should be drafted.\n"
        "- Call ReviewAgent if a report is ready for feedback.\n"
        "You do not do the actual work yourself — you delegate to the right agent."
    ),
    llm=llm,
    can_handoff_to=["ResearchAgent", "WriteAgent", "ReviewAgent"],
)
