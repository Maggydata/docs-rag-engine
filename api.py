from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from retrieval.vector_store import load_vector_store
from rag.graph import build_rag_graph
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

class ChatRequest(BaseModel) :
    question : str
    thread_id : str | None = None
    

class Source(BaseModel) : 
    heading : str
    content : str    
    
    
class ChatResponse(BaseModel):
    answer : str
    thread_id : str
    sources : list[Source]
    
    

embedder = OpenAIEmbeddings(model = "text-embedding-3-small")
store = load_vector_store(embedder)
llm = ChatOpenAI(model = "gpt-4o-mini")
graph = build_rag_graph(store, llm, k=6)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post("/chat", response_model = ChatResponse)
def chat(req : ChatRequest) -> ChatResponse : 
    
    #The backend creates the thread_id if it doesn't exist
    thread_id = req.thread_id or str(uuid.uuid4())
    
    config = {"configurable" : {"thread_id" : thread_id}}
    result = graph.invoke({"messages" : [("user", req.question)]}, config)
    
    answer = result["messages"][-1].content
    
    sources = [
        Source(heading = c.metadata.get("heading", ""), content = c.page_content)
        for c in result["retrieved_chunks"]
    ]
    
    return ChatResponse(answer = answer, thread_id = thread_id, sources = sources)
    
    