
# Multi-Agent Workflow API

This project is a **FastAPI application** that runs a **multi-agent workflow** using [LlamaIndex](https://docs.llamaindex.ai/), OpenAI models, and Tavily search.
It allows you to chat with a coordinator agent that delegates tasks to specialized agents (Research, Write, Review).
The app supports multiple sessions with memory.



## Features

* **Multi-agent workflow**:

  * ResearchAgent – gathers and analyzes information
  * WriteAgent – drafts structured reports
  * ReviewAgent – reviews reports and provides improvements
  * MainAgent – coordinates everything

* **Session management**

  * Create, list, delete, and restore sessions
  * In-memory context storage
  * Mongodb context memory storage

* **Endpoints**

  * `POST /chat` – Send a message and get a response
  * `GET /sessions` – List all sessions
  * `GET /sessions/{id}` – Get info for one session
  * `DELETE /sessions/{id}` – Delete a session
  * `GET /stats` – App usage statistics
  * `GET /` – Health check

---

## Project Structure

```
llamaindex_multi_agent_app/
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── agents/
│   │   ├── agents.py
│   │   ├── tools.py
│   │   └── workflow.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── sessions.py
│   │   └── stats.py
│   └── utils.py
├── readme.MD
├── requirements.txt
└── run.py
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

