from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from datetime import datetime
from typing import Optional
from ..models import ChatRequest, ChatResponse
from ..utils import create_session_id, get_or_create_context, save_context
from ..agents.workflow import agent_workflow
from ..config import logger
from docling.document_converter import DocumentConverter

router = APIRouter()
converter = DocumentConverter()

@router.post("/chat", response_model=ChatResponse)
async def chat( 
    session_id: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),     
):
    try:
        request = ChatRequest(session_id=session_id, message=message)
        session_id = request.session_id or create_session_id()
        ctx = get_or_create_context(session_id)

        logger.info(f"Session {session_id} - User message: {request.message}")
        
        # Handle file upload
        if file:
            logger.info(f"Processing uploaded file: {file.filename}")
            try:
                # Save temporarily
                file_path = f"/tmp/{file.filename}"
                with open(file_path, "wb") as f:
                    f.write(await file.read())

                # Convert document
                result = converter.convert(file_path)
                document = result.document
                markdown_output = document.export_to_markdown()
                logger.info(f"Extracted {len(markdown_output)} characters from {file.filename}")
                #TODO: you can set up a RAG Pipeline here with the markdown_output
                # RAG Pipeline:
                # 1. Extraction
                # 2. Chunking
                # 3. Embedding
                # 4. Searching
                # 5. Answering/chatting


            except Exception as e:
                logger.error(f"Docling conversion failed: {str(e)}", exc_info=True)
                raise HTTPException(status_code=400, detail="Invalid file format")

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
