

🏍️ MyBikeBuddy

An agentic RAG (Retrieval-Augmented Generation) motorcycle troubleshooting assistant that helps you diagnose and fix bike issues through a conversational interface.

Built with FastAPI, LangChain/LangGraph, Google Gemini, Tavily web search, and Qdrant vector search, with persistent conversation history and an interactive web UI. Deployed on Render.

🔗 Live Demo: my-bike-buddy-1.onrender.com

---

✨ Features

· Agentic RAG Pipeline — Uses LangGraph to reason over retrieved context, making multi-step decisions rather than simple one-shot retrieval.
· Gemini-Powered Reasoning — Google Gemini LLM drives the agent's decision-making and answer generation.
· Hybrid Retrieval — Combines Qdrant vector search over a curated knowledge base with Tavily web search for fresh, real-time information.
· Conversation Persistence — SQLite-backed chat history so you can pick up where you left off.
· Graph Checkpointing — LangGraph checkpoint DB for resumable agent state.
· Interactive Web UI — Clean HTML/CSS/JS frontend served directly by FastAPI.
· Dockerized — One-command local deployment with docker-compose.
· Cloud Deployed — Live on Render.

---

🏗️ Architecture

```
User (Web UI)
     │
     ▼
FastAPI (main.py)
     │
     ├──► LangGraph Agent (retrival_graph.py)
     │         │
     │         ├──► Qdrant Vector Store  ──► local knowledge base
     │         ├──► Tavily Web Search    ──► live web results
     │         └──► Google Gemini LLM    ──► reasoning & generation
     │
     ├──► SQLite (bikehelper.db) — conversation history
     └──► Checkpoint DB (graphcheckpoint_db.py) — agent state
```

---

📁 Project Structure

File / Folder Purpose
main.py FastAPI application entry point & API routes
run.py Server runner / startup script
retrival_graph.py LangGraph agent definition & retrieval logic
graphcheckpoint_db.py LangGraph state checkpoint persistence
ingest.py Data ingestion script — loads & embeds docs into Qdrant
common.py Shared utilities/config
static/ Frontend assets (HTML/CSS/JS)
data/ Source data for the knowledge base
bikehelper.db SQLite database for chat history
dockerfile / docker-compose.yml Containerization & local deployment
requirements.txt Python dependencies

---

🚀 Getting Started

Prerequisites

· Python 3.10+
· Qdrant instance (local or cloud)
· A Google Gemini API key from Google AI Studio
· A Tavily API key from tavily.com

1. Clone the repository

```bash
git clone https://github.com/aalu-leloo/my_bike_buddy.git
cd my_bike_buddy
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

Create a .env file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_key
```

Adjust variable names to match what your code actually reads in common.py.

5. Ingest the knowledge base

```bash
python ingest.py
```

6. Run the application

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in your browser.

---

🐳 Docker (Local Deployment)

```bash
docker-compose up --build
```

This spins up the app (and Qdrant, if configured in docker-compose.yml) with a single command.

---

☁️ Deployment on Render

The project is live at my-bike-buddy-1.onrender.com.

Steps to deploy your own instance

1. Push the repo to GitHub.
2. On Render, click New → Web Service and connect the repository.
3. Configure the service:
   · Environment: Docker (recommended, since a dockerfile is included)
   · Build Command: (handled by Docker)
   · Start Command: (handled by Docker / or uvicorn main:app --host 0.0.0.0 --port $PORT)
4. Add the following Environment Variables in the Render dashboard:
   Key Value
   GOOGLE_API_KEY your Gemini API key
   TAVILY_API_KEY your Tavily API key
   QDRANT_URL your Qdrant cloud URL
   QDRANT_API_KEY your Qdrant API key
5. Deploy — Render will build and serve the app automatically.

⚠️ Note: Render's filesystem is ephemeral. SQLite files (bikehelper.db, checkpoint DB) will reset on redeploy unless you attach a persistent disk or migrate to a managed DB. See the Render disks docs for details.

---

🛠️ Tech Stack

Layer Technology
API FastAPI
Agent Orchestration LangChain / LangGraph
LLM Google Gemini
Web Search Tavily
Vector Database Qdrant
Persistence SQLite
Frontend HTML / CSS / JavaScript
Local Deployment Docker, Docker Compose
Cloud Hosting Render

---

🔌 API Endpoints

Update these to match your actual routes in main.py.

Method Endpoint Description
GET / Serves the web UI
POST /chat Send a message, receive agent response
GET /history/{session_id} Retrieve past conversation

---

📄 License

Apache
---

🙏 Acknowledgements

· Google Gemini
· Tavily
· LangChain & LangGraph
· Qdrant
· FastAPI
· Render
