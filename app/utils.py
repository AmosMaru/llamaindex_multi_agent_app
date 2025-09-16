import uuid
from datetime import datetime
from typing import Dict
from llama_index.core.workflow import Context, JsonSerializer
from .workflow import agent_workflow
from .config import logger

# In-memory session storage
session_contexts: Dict[str, dict] = {}
session_metadata: Dict[str, dict] = {}

def create_session_id() -> str:
    session_id = str(uuid.uuid4())
    logger.info(f"Created new session: {session_id}")
    return session_id

def get_or_create_context(session_id: str) -> Context:
    if session_id in session_contexts:
        logger.info(f"Restoring context for session {session_id}")
        ctx_dict = session_contexts[session_id]
        return Context.from_dict(agent_workflow, ctx_dict, serializer=JsonSerializer())
    else:
        logger.info(f"Creating new context for session {session_id}")
        ctx = Context(agent_workflow)
        session_metadata[session_id] = {
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "message_count": 0
        }
        return ctx

def save_context(session_id: str, ctx: Context):
    logger.info(f"Saving context for session {session_id}")
    session_contexts[session_id] = ctx.to_dict(serializer=JsonSerializer())
    if session_id in session_metadata:
        session_metadata[session_id]["last_activity"] = datetime.now()
        session_metadata[session_id]["message_count"] += 1
