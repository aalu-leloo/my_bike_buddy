import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from common import embeddings,collection,qdrant_url
def main():
    data=json.load(open("data/solution.json", encoding="utf_8"))
    docs=[
    Document(
        page_content=f"problem:{d["problem"]}\nSymptoms:{d["symptoms"]}\n Solution:{d['solution']}",metadata={"problem":d["problem"]}
    )
    for d in data
]
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
    chunk=splitter.split_documents(docs)

    QdrantVectorStore.from_documents(
        chunk,
        embeddings,
        url=qdrant_url,
        collection_name=collection,
        force_recreate=True,
    )
    print(f"Indexed{len(chunk)} from {len(docs)} entries")

if __name__=="__main__":
     main()