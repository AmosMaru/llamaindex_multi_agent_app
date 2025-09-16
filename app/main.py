from fastapi import FastAPI
from .routes import chat, sessions, stats

app = FastAPI(
    title="Multi-Agent Workflow API",
    description="FastAPI application with multi-agent workflow and memory",
    version="2.0.0"
)

@app.get("/")
async def root():
    return {"message": "Multi-Agent Workflow API is running", "status": "healthy"}

# Routers
app.include_router(chat.router)
app.include_router(sessions.router)
app.include_router(stats.router)
