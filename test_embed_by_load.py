from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings
from retrieval.vector_store import load_vector_store

embedder = OpenAIEmbeddings(model="text-embedding-3-small")
store = load_vector_store(embedder, persist_directory="./chroma_db")

# --- questions ---
for question in [
    "checkpointer InMemorySaver thread_id conversational memory",
    "MMR maximum marginal relevance diversity search_type"
]:
    print(f"\nQ: {question}")
    for r in store.similarity_search(question, k=3):
        print(f"  [{r.metadata['heading']}] {r.page_content[:150]}...")