from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from retrieval.vector_store import load_vector_store
from rag.graph import build_rag_graph

embedder = OpenAIEmbeddings(model="text-embedding-3-small")
store = load_vector_store(embedder)          # Reload the index; do not re-embed
llm = ChatOpenAI(model="gpt-4o-mini")        # or whichever model you want

graph = build_rag_graph(store, llm, k=6)

result = graph.invoke({"question": "How does tool calling work in LangChain?"})
for r in result["retrieved_chunks"]:
    print(f"[{r.metadata['heading']}] {r.page_content[:100]}")
print("\n---\n", result["response"])