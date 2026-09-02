from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings
from retrieval.vector_store import load_vector_store

embedder = OpenAIEmbeddings(model="text-embedding-3-small")
store = load_vector_store(embedder, persist_directory="./chroma_db")

results = store.similarity_search("What is tool calling?", k=1)
print(results[0].metadata["heading"], "|", results[0].page_content[:80])