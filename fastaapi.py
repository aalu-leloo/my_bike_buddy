from fastaapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from graphcheckpoint_db import init_db, get_history
from retrival_graph import graph

app = FastAPI()
init_db()

class Ask(BaseModel):
    query: str

@app.post("/api/ask")
def ask(body: Ask):
    out = graph.invoke({"query": body.query})
    return {"answer": out["answer"], "source": out["source"]}

@app.get("/api/history")
def history():
    return get_history()

app.mount("/", StaticFiles(directory="static", html=True), name="static")