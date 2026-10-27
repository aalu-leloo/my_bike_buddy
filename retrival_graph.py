
from typing import TypedDict
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END

from common import embeddings, llm, collection,qdrant_url,threshold
from db import save_chat
# tools
client=QdrantClient(url=qdrant_url)
vectorstore=QdrantVectorStore(client=client,collection_name=collection,embedding=embeddings)
web_tool=TavilySearch(max_result=4)
prompt=ChatPromptTemplate.from_template(
     """You are BikeHelper, a motorcycle troubleshooting assistant.
Rider's problem: {query}

Reference info (from {source}):
{context}

Analyse the problem and give clear steps. End by advising the rider
to contact an authorised service center."""
)
chain = prompt | llm | StrOutputParser()
class state(TypedDict):
    query:str
    context:str
    source:str
    score:float
    answer:str
#nodes
def retrieve(state: state):
    results = vectorstore.similarity_search_with_score(state["query"], k=3)
    score = results[0][1] if results else 0.0
    print("top score:", round(score, 3))
    context = "\n\n".join(doc.page_content for doc, _ in results)
    return {"context": context, "score": score, "source": "database"}

def web_search(state: state):
    res = web_tool.invoke({"query": f"motorcycle {state['query']}"})
    context = "\n\n".join(f"{r['title']}: {r['content']}" for r in res["results"])
    return {"context": context, "source": "web"}

def generate(state: state):
    text = chain.invoke({
        "query": state["query"],
        "source": state["source"],
        "context": state["context"],
    })
    return {"answer": text}

def save(state: state):
    save_chat(state["query"], state["answer"], state["source"], state.get("score", 0.0))
    return {}

# --- routing ---
def route(state: state):
    return "generate" if state["score"] >= threshold else "web_search"
builder=StateGraph(state)
builder.add_node("retrieve", retrieve)
builder.add_node("web_search", web_search)
builder.add_node("generate", generate)
builder.add_node("save", save)
builder.add_edge(START, "retrieve")
builder.add_conditional_edges("retrieve", route, {"generate": "generate", "web_search": "web_search"})
builder.add_edge("web_search", "generate")
builder.add_edge("generate", "save")
builder.add_edge("save", END)

graph = builder.compile()