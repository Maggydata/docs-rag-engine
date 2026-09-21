from dotenv import load_dotenv; load_dotenv()
from langchain_openai import OpenAIEmbeddings
from retrieval.vector_store import load_vector_store


store = load_vector_store(OpenAIEmbeddings(model="text-embedding-3-small"))
for c in store.similarity_search("with_structured_output response_format create_agent structured_response", k=5):
    print(f"[{c.metadata['heading']}] {c.page_content[:80]}")