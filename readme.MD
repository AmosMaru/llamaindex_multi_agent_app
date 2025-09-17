
# Multi-Agent Workflow API

This project is a **FastAPI application** that runs a **multi-agent workflow** using [LlamaIndex](https://docs.llamaindex.ai/), OpenAI models, and Tavily search.
It allows you to chat with a coordinator agent that delegates tasks to specialized agents (Research, Write, Review).
The app supports multiple sessions with memory and document processing capabilities.

## Features

* **Multi-agent workflow**:
  * **MainAgent** – Coordinator that delegates to specialized agents
  * **ResearchAgent** – Gathers and analyzes information using web search
  * **WriteAgent** – Drafts structured reports and content
  * **ReviewAgent** – Reviews reports and provides improvements

* **Document Processing**:
  * File upload support via `/chat` endpoint
  * Document conversion using Docling (PDF, Word, etc.)
  * Automatic extraction to markdown format
  * RAG pipeline ready (extraction, chunking, embedding, searching)

* **Session Management**:
  * Create, list, delete, and restore sessions
  * Persistent context storage with MongoDB
  * Session-based memory across conversations

* **API Endpoints**:
  * `POST /chat` – Send messages and upload files for processing
  * `GET /sessions` – List all active sessions
  * `GET /sessions/{id}` – Get information for a specific session
  * `DELETE /sessions/{id}` – Delete a session
  * `GET /stats` – App usage statistics
  * `GET /` – Health check

---

## Project Structure

```
llamaindex_multi_agent_app/
├── .env                          # Environment variables
├── .gitignore                    # Git ignore file
├── app/                          # Main application package
│   ├── __init__.py
│   ├── agents/                   # Agent definitions and workflow
│   │   ├── agents.py            # Agent implementations (Main, Research, Write, Review)
│   │   ├── tools.py             # Tools for agents (web search, etc.)
│   │   └── workflow.py          # Agent workflow configuration
│   ├── config.py                # Configuration and environment setup
│   ├── models.py                # Pydantic models for API
│   ├── routes/                  # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── chat.py              # Chat endpoint with file upload
│   │   ├── sessions.py          # Session management endpoints
│   │   └── stats.py             # Statistics endpoints
│   └── utils.py                 # Utility functions
├── readme.MD                    # This file
├── requirements.txt             # Python dependencies
└── run.py                       # Application entry point
```

---

## Setup

1. **Clone repo**

   ```bash
   git clone https://github.com/AmosMaru/llamaindex_multi_agent_app

   cd llamaindex_multi_agent_app
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   Create a `.env` file with your keys:

   ```env
   OPENAI_API_KEY=sk-xxxx
   TAVILY_API_KEY=tv-xxxx
   ```

4. **Run the server**

   ```bash
   python run.py
   ```

Server runs at: [http://localhost:8000](http://localhost:8000)

---

## Example Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Write me a report about renewable energy"}'
```

