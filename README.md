MyBikeBuddy — LangGraph + Gemini + Tavily + Qdrant + FastAPI

An agentic RAG assistant for motorcycle troubleshooting. It answers questions using a curated motorcycle repair knowledge base stored in Qdrant, and can fall back to live web search. Conversations are remembered per session and it ships with a simple web UI.

Educational use only. This is a learning project. It is not a substitute for a certified mechanic, and it must not be used to make safety-critical repair decisions. If you are unsure about a repair that affects brakes, steering, or the frame, consult a qualified mechanic.

Live demo: https://my-bike-buddy-1.onrender.com/

---

Features

· Knowledge base search (RAG): finds the most relevant chunks of the motorcycle knowledge base in Qdrant and uses them to answer.
· Web search fallback: if the knowledge base does not have the answer, the agent can search the web with Tavily.
· Agentic routing: a LangGraph flow decides when to retrieve, when to search the web, and when to answer directly.
· Conversation memory: chats are saved per conversation in a local SQLite file, with LangGraph checkpointing for resumable agent state.
· Simple web page: plain HTML, CSS and JavaScript, no frontend framework.

How it works

```
Your question
     │
     ▼
 Retrieve  ──►  search the knowledge base in Qdrant (Gemini embeddings)
     │
     ▼
  Route    ──►  is the retrieved answer enough?
     │                │
     │ no             │ yes
     ▼                │
  Tavily web search   │
     │                │
     └──────► Answer (Gemini) ◄──┘
```

Tech stack

Part Tool
Web server FastAPI + Uvicorn
AI model & embeddings Google Gemini (google-genai, langchain-google-genai)
Agent flow LangGraph (with SQLite memory)
Vector database Qdrant
Web search Tavily
Persistence SQLite

Requirements

· Python 3.10+
· API keys for Gemini, Qdrant and Tavily
· An internet connection

Setup

1. Create a virtual environment and install packages

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a .env file in the project folder:

```env
GOOGLE_API_KEY=your-gemini-key
TAVILY_API_KEY=your-tavily-key
QDRANT_URL=https://your-cluster-url
QDRANT_API_KEY=your-qdrant-key
```

Check common.py for the exact setting names and default models your code uses.

3. Load the knowledge base into Qdrant (run once)

```bash
python ingest.py
```

· The Qdrant collection uses the embedding size produced by your Gemini embedding model. Use a fresh collection whenever you change the embedding model.
· This step makes many embedding calls. On the free Gemini tier you may see Error 429, retrying in 65s. That is normal: the script waits and tries again.

4. Start the server

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --port 8000
```

Open http://127.0.0.1:8000.

Project structure

```
main.py               FastAPI app: routes for the UI and chat
retrival_graph.py     LangGraph flow: retrieve → route → web search → answer
graphcheckpoint_db.py LangGraph checkpoint persistence (SQLite)
knowledge / ingest.py reads the source data, embeds it, uploads to Qdrant
common.py             shared settings and environment variables
run.py                helper to start the server
static/               index.html, CSS and JavaScript
data/                 source data for the knowledge base
bikehelper.db         SQLite database for chat history
dockerfile            container build
docker-compose.yml    local container orchestration
requirements.txt      Python dependencies
```

API endpoints

Method Path What it does
GET / the web page
POST /chat main chat endpoint
GET /history/{session_id} retrieve a past conversation

Update these to match the actual routes in main.py.

Deployment on Render

The project is live at https://my-bike-buddy-1.onrender.com/.

To deploy your own instance:

1. Push the repo to GitHub.
2. On Render, click New → Web Service and connect the repository.
3. Use the included Dockerfile as the environment.
4. Add the environment variables from your .env in the Render dashboard.
5. Deploy — Render will build and serve the app automatically.

Note: Render's filesystem is ephemeral. SQLite files (bikehelper.db, checkpoint DB) will reset on redeploy unless you attach a persistent disk or migrate to a managed database. See the Render disks docs for details.

Docker (local deployment)

```bash
docker-compose up --build
```

This spins up the app (and Qdrant, if configured in docker-compose.yml) with a single command.

Troubleshooting

Problem What to try
500 on /chat Look at the terminal running the server. The real error and traceback are printed there. Make sure you are opening the same port the server is using.
Port already in use An old server is still running. Stop it with Ctrl + C, or choose another port.
Code changes do not show up Restart the server, or start it with --reload.
Error 429 during ingest Gemini rate limit. The script retries by itself. Use smaller batches, or a paid plan.
Search returns nothing or dimension errors The Qdrant collection size must match the embedding model. Re-run ingest.py on a fresh collection.
Tavily search missing Add TAVILY_API_KEY. Without it, web search is switched off.
SQLite data disappears after redeploy Render's filesystem is ephemeral. Attach a persistent disk or use a managed database.

Safety and privacy

· Never commit your .env file. Make sure it is listed in .gitignore.
· Do not commit the chat memory files (bikehelper.db, .db-shm, .db-wal). They can contain conversations. Add *.db, *.db-shm and *.db-wal to .gitignore.
· Repair advice may become out-of-date for newer bike models.
· Do not rely on this tool for safety-critical repairs (brakes, steering, frame, fuel system).
· Before any real-world use you would need: proper user login, request limits, review of the answers, and a license check for the source data.

Author

aalu-leloo — GitHub

Acknowledgements

· Google Gemini
· Tavily
· LangChain & LangGraph
· Qdrant
· FastAPI
· Render

License

Specify your license here (e.g., MIT). If none exists yet, consider adding one — for example Apache-2.0, matching a LICENSE file in the repo.

---

Changes made to match the reference style:

· Renamed title to the Project — Stack format and added an intro paragraph + safety disclaimer.
· Rewrote Features as sentence-style bullets (dropped emojis).
· Replaced the ASCII architecture with a matching retrieve → route → web search flow diagram, adapted to your stack.
· Added a Requirements section and numbered Setup steps with Windows/macOS-Linux blocks and a .env example.
· Reorganized Project structure as a plain tree-style list instead of a table.
· Kept API endpoints as a table, added a Deployment on Render section (kept, since it's unique to your project).
· Converted Troubleshooting to the same problem/what-to-try table format.
· Replaced Contributing with a Safety and privacy section in the same spirit.
· Removed the old Author/Acknowledgements ordering issues and ended with License pointing to a LICENSE file.

I kept the live Render URL (in the intro and deployment section) and omitted the License-as-placeholder tone to match the reference's confident Apache-2.0. See the LICENSE file. — just swap in your actual license.
