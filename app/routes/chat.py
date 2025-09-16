from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..models import ChatRequest, ChatResponse
from ..utils import create_session_id, get_or_create_context, save_context
from ..workflow import agent_workflow
from ..config import logger

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.session_id or create_session_id()
        ctx = get_or_create_context(session_id)

        logger.info(f"Session {session_id} - User message: {request.message}")

        response = await agent_workflow.run(user_msg=request.message, ctx=ctx)

        logger.info(f"Session {session_id} - Final response: {response}")

        save_context(session_id, ctx)

        return ChatResponse(
            response=str(response),
            session_id=session_id,
            timestamp=datetime.now(),
        )
    except Exception as e:
        logger.error(f"Error in /chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
