from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from retrieval.vector_store import load_vector_store
from rag.graph import build_rag_graph

embedder = OpenAIEmbeddings(model="text-embedding-3-small")
store = load_vector_store(embedder)
llm = ChatOpenAI(model="gpt-4o-mini")
graph = build_rag_graph(store, llm, k=6)

config = {"configurable": {"thread_id": "conv_1"}}  

r1 = graph.invoke({"messages": [("user", "How does tool calling work in LangChain?")]}, config)
print("T1:", r1["messages"][-1].content[:200])

r2 = graph.invoke({"messages": [("user", "Can you give me a concrete example of it?")]}, config)
print("\nT2:", r2["messages"][-1].content[:300])