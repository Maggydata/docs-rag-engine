from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from ingestion.models import Chunk

def build_vector_store(chunks: list[Chunk], embedder: Embeddings, persist_directory: str= "./chroma_db") -> Chroma:
    
    """
    Build a vector store from a list of chunks and an embedder.

    Args:
        chunks (list[Chunk]): A list of Chunk objects to be added to the vector store.
        embedder (Embeddings): An embedding model to convert text into vector representations.
        persist_directory (str): The directory where the vector store will be persisted.
        
    Returns: 
        Chroma: The built and persisted vector store.    

    """
    
    texts = [f"{c.heading}\n\n{c.content}" for c in chunks]
    
    metadatas = [{"source_id" : c.source_id, "heading" : c.heading} for c in chunks]
    
    return Chroma.from_texts(
        persist_directory=persist_directory,
        embedding=embedder,
        texts=texts,
        metadatas=metadatas)
    
def load_vector_store(embedder: Embeddings, persist_directory: str= "./chroma_db" ) -> Chroma:
    
    """
    Load a persisted vector store from a specified directory.

    Args:
        persist_directory (str): The directory where the vector store is persisted.
        embedder (Embeddings):the embedding model used to embed queries at search time.

    Returns:
        Chroma: The loaded vector store.
    """
    
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedder)    
