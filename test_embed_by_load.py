from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings
from retrieval.vector_store import load_vector_store

embedder = OpenAIEmbeddings(model="text-embedding-3-small")
store = load_vector_store(embedder, persist_directory="./chroma_db")

# --- questions ---
for question in [
    "How does tool calling work in LangChain?"
]:
    print(f"\nQ: {question}")
    for r in store.similarity_search(question, k=8):
        if r.metadata["heading"] == "History":
            print(r.page_content)
        #print(f"  [{r.metadata['heading']}] {r.page_content[:80]}...")