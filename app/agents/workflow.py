from llama_index.core.agent.workflow import AgentWorkflow
from .agents import main_agent, research_agent, write_agent, review_agent

agent_workflow = AgentWorkflow(
    agents=[main_agent, research_agent, write_agent, review_agent],
    root_agent=main_agent.name,
    initial_state={
        "research_notes": {},
        "report_content": "Not written yet.",
        "review": "Review required.",
    },
)
