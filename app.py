import streamlit as st
import uuid
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from retrieval.vector_store import load_vector_store
from rag.graph import build_rag_graph

@st.cache_resource
def load_graph():
    embedder = OpenAIEmbeddings(model = "text-embedding-3-small")
    store = load_vector_store(embedder)
    llm = ChatOpenAI(model = "gpt-4o-mini")
    return build_rag_graph(store, llm, k=6)

graph = load_graph()

st.title("docs-rag-engine")

if "messages" not in st.session_state :
    st.session_state.messages = []

if "thread_id" not in st.session_state :
    st.session_state.thread_id = str(uuid.uuid4())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
question = st.chat_input("Ask about Langchain ...")      


if question :
    # save and show user question
    st.session_state.messages.append({"role": "user", "content" : question})
    with st.chat_message("user") : 
        st.markdown(question)
      
    # invoke the graph with the thread_id session
    config = {"configurable" : {"thread_id" : st.session_state.thread_id}}
    with st.spinner("Thinking..."):
        result =   graph.invoke({"messages" : [("user", question)]}, config)
      
    #extract answer
    answer = result["messages"][-1].content
      
    #save and show answer
    st.session_state.messages.append({"role" : "assistant", "content" : answer})
    with st.chat_message("assistant"):
        st.markdown(answer)