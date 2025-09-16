import uuid
from datetime import datetime
from typing import Dict
from llama_index.core.workflow import Context, JsonSerializer
from .agents.workflow import agent_workflow
from .config import logger, context_collection, metadata_collection

# In-memory cache (optional, for faster access)
session_contexts: Dict[str, dict] = {}
session_metadata: Dict[str, dict] = {}

def create_session_id() -> str:
    session_id = str(uuid.uuid4())
    logger.info(f"Created new session: {session_id}")
    return session_id

def get_or_create_context(session_id: str) -> Context:
    # 1  First check in-memory
    if session_id in session_contexts:
        logger.info(f"Restoring context from memory for session {session_id}")
        ctx_dict = session_contexts[session_id]
        return Context.from_dict(agent_workflow, ctx_dict, serializer=JsonSerializer())

    # 2 Then check MongoDB
    db_record = context_collection.find_one({"session_id": session_id})
    if db_record:
        logger.info(f"Restoring context from MongoDB for session {session_id}")
        ctx_dict = db_record["context"]
        session_contexts[session_id] = ctx_dict
        return Context.from_dict(agent_workflow, ctx_dict, serializer=JsonSerializer())

    # 3 Otherwise create new
    logger.info(f"Creating new context for session {session_id}")
    ctx = Context(agent_workflow)
    metadata = {
        "session_id": session_id,
        "created_at": datetime.now(),
        "last_activity": datetime.now(),
        "message_count": 0,
    }
    session_metadata[session_id] = metadata
    metadata_collection.insert_one(metadata)
    return ctx

def save_context(session_id: str, ctx: Context):
    logger.info(f"Saving context for session {session_id}")
    ctx_dict = ctx.to_dict(serializer=JsonSerializer())

    # Save in memory
    session_contexts[session_id] = ctx_dict

    # Save in MongoDB
    context_collection.update_one(
        {"session_id": session_id},
        {"$set": {"context": ctx_dict}},
        upsert=True
    )

    # Update metadata
    if session_id in session_metadata:
        session_metadata[session_id]["last_activity"] = datetime.now()
        session_metadata[session_id]["message_count"] += 1
        metadata_collection.update_one(
            {"session_id": session_id},
            {"$set": session_metadata[session_id]},
            upsert=True
        )
