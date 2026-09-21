from typing import Annotated, TypedDict
from langchain_core.documents import Document
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


class RAGState(TypedDict):
    """
    RAGState is a dictionary that holds the state of a RAG (Retrieval-Augmented Generation) model.
    It contains the following keys:
    - 'messages': A list of messages exchanged in the conversation.
    - 'retrieved_chunks': A list of chunks retrieved from the knowledge base.
    """
    messages : Annotated[list, add_messages]
    retrieved_chunks : list[Document]
    search_query : str
    

def make_reformulate_node(llm): 
    def reformulate(state : RAGState) -> dict:
        messages = state["messages"]
        
        if len(messages) <= 1 :
            return {"search_query" : messages[-1].content}
        
        system = ("Here is a conversation. "
                  "Rewrite the last question as a concise, standalone search query, "
                  "including the necessary context. "
                  "Do NOT answer the question; generate ONLY the query.")
        
        messages_to_reformulate = [("system", system)] + messages
        response = llm.invoke(messages_to_reformulate)
        return {"search_query" : response.content}
    
    return reformulate

 
def make_retrieve_node(store, k:int = 3):
    def retrieve(state : RAGState) -> dict:
        question = state["search_query"]
        chunks = store.similarity_search(question, k=k)
        return {"retrieved_chunks" : chunks}  
    return retrieve
            

def make_generate_node(llm): 
    def generate(state: RAGState) -> dict : 
        chunks = state["retrieved_chunks"]
        parts = [c.page_content for c in chunks]
        context =  "\n\n".join(parts)

        system = ("Answer questions about the LangChain documentation based only on the context provided. "
                    "If the context explains the relevant concept but lacks a specific code example, "
                    "explain the concept using the available information and note that a precise code "
                    "example isn't available. "
                    "Only if the context is unrelated to the question, say you don't have the answer.\n\n"
                    "Context:\n" + context)
        
        messages = [("system", system)] + state["messages"]
        response = llm.invoke(messages)
        
        return {"messages" : [response]}
    
    return generate


def build_rag_graph(store, llm, k: int = 3):
    """
    Builds a RAG (Retrieval-Augmented Generation) graph using the provided store and LLM (Language Model).
    
    Args:
        store: The knowledge store used for retrieving relevant chunks.
        llm: The language model used for generating responses.
        k: The number of chunks to retrieve from the store (default is 3). 
    
    Returns:
        The compiled RAG graph, ready to be invoked.    
    
    """
    
    builder = StateGraph(RAGState)
    
    builder.add_node("reformulate", make_reformulate_node(llm))
    builder.add_node("retrieve", make_retrieve_node(store, k))
    builder.add_node("generate", make_generate_node(llm))
    
    builder.add_edge(START, "reformulate")
    builder.add_edge("reformulate", "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)
    
    checkpointer = MemorySaver()
    
    return builder.compile(checkpointer = checkpointer)