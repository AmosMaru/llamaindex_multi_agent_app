from fastapi import APIRouter
from ..utils import session_metadata, session_contexts

router = APIRouter()

@router.get("/stats")
async def get_stats():
    total_sessions = len(session_metadata)
    active_contexts = len(session_contexts)
    total_messages = sum(metadata["message_count"] for metadata in session_metadata.values())
    return {
        "total_sessions": total_sessions,
        "active_contexts": active_contexts,
        "total_messages": total_messages,
        "avg_messages_per_session": total_messages / max(total_sessions, 1)
    }
