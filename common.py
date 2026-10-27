import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
load_dotenv()
key=os.getenv("GEMINI_API_KEY")
qdrant_url=os.getenv("QDRANT_URL")
collection=os.getenv("COLLECTION")
threshold=float(os.getenv("THRESHOLD", "0.6"))
model1=os.getenv("GEMINI_CHAT_MODEL")
model2=os.getenv("GEMINI_EMBED_MODEL")
embeddings=GoogleGenerativeAIEmbeddings(model=model2,google_api_key=key)
llm=ChatGoogleGenerativeAI(model=model1,google_api_key=key)
tavily_key=os.getenv("TAVILY_API_KEY")
