from fastapi import APIRouter, HTTPException
from ..utils import session_metadata, session_contexts
from ..models import SessionInfo, SessionListResponse
from ..config import logger

router = APIRouter()

@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions():
    sessions = []
    for session_id, metadata in session_metadata.items():
        sessions.append(SessionInfo(
            session_id=session_id,
            created_at=metadata["created_at"],
            last_activity=metadata["last_activity"],
            message_count=metadata["message_count"]
        ))
    return SessionListResponse(sessions=sessions)

@router.get("/sessions/{session_id}")
async def get_session_info(session_id: str):
    if session_id not in session_metadata:
        raise HTTPException(status_code=404, detail="Session not found")
    metadata = session_metadata[session_id]
    return {
        "session_id": session_id,
        "created_at": metadata["created_at"],
        "last_activity": metadata["last_activity"],
        "message_count": metadata["message_count"],
        "has_context": session_id in session_contexts
    }

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    if session_id not in session_metadata:
        raise HTTPException(status_code=404, detail="Session not found")
    if session_id in session_contexts:
        del session_contexts[session_id]
    del session_metadata[session_id]
    logger.info(f"Deleted session {session_id}")
    return {"message": f"Session {session_id} deleted successfully"}
