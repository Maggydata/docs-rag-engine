from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from ingestion.batch import ingest_corpus
from ingestion.chunking import chunk_document
from retrieval.vector_store import build_vector_store

report = ingest_corpus(Path("data-source/src/oss/langchain"))
all_chunks = []
for doc in report.documents:
    all_chunks.extend(chunk_document(doc))
print(f"{len(all_chunks)} chunks to index.")

embedder = OpenAIEmbeddings(model="text-embedding-3-small")
store = build_vector_store(all_chunks, embedder, persist_directory="./chroma_db")
print("Index construit.")

# --- questions ---
for question in [
    "How do I stream tokens from a model?",
    "What is tool calling?",
    "How does structured output work?",
]:
    print(f"\nQ: {question}")
    for r in store.similarity_search(question, k=2):
        print(f"  [{r.metadata['heading']}] {r.page_content[:80]}...")