eval_questions = [
    {
        "question" : "Which class allows you to split text recursively?",
        "reference" : "The RecursiveCharacterTextSplitter class, imported from langchain_text_splitters, recursively splits text on common separators such as newlines until each chunk reaches the target size, and it is the recommended splitter for generic text use cases."
    },
    {
            "question" : "How do you turn a Python function into a tool that an agent can use?",
            "reference" : "You decorate the function with @tool, imported from langchain.tools, and by default the function's docstring becomes the tool's description, while type hints are required because they define the tool's input schema."
        },
    {
            "question" : "Which environment variables enable LangSmith tracing?",
            "reference" : "You need to set LANGSMITH_TRACING to 'true' and provide your API key in LANGSMITH_API_KEY."
        },
    {
            "question" : "How do you initialize a chat model without depending on a specific provider?",
            "reference" : "You use the init_chat_model() function from langchain.chat_models, and you can specify both the model and its provider in a single argument using the '{model_provider}:{model}' format, for example 'openai:o1'."
        },
    {
            "question" : "Which method turns a vector store into a retriever?",
            "reference" : "The as_retriever method returns a VectorStoreRetriever that exposes search_type and search_kwargs, and it supports the search types 'similarity' (the default), 'mmr', and 'similarity_score_threshold'."
        },
    {
            "question" : "What is the difference between invoke, stream, and batch?",
            "reference" : "The invoke method returns a complete response after the model has finished generating, stream returns the output progressively as chunks while it is being generated, and batch sends multiple independent requests that are processed in parallel on the client side."
        },
    {
            "question" : "What is MMR search and when should you use it?",
            "reference" : "MMR, or maximum marginal relevance, is a search method that balances similarity with diversity in the results, and it can be selected on a retriever with search_type='mmr'."
        },
    {
            "question" : "Why should PDF pages be split into smaller chunks before indexing?",
            "reference" : "A single page is often too coarse for retrieval, so splitting it into smaller chunks prevents relevant passages from being diluted by surrounding text, and the add_start_index=True option keeps each chunk's character offset in its metadata."
        },
    {
            "question" : "What is the difference between ToolStrategy and ProviderStrategy for structured output?",
            "reference" : "ToolStrategy produces structured output through tool calling, while ProviderStrategy uses the provider's native structured output, and when you pass a schema directly, LangChain picks ProviderStrategy if the model supports it and falls back to ToolStrategy otherwise."
        },
    {
            "question" : "When should you use Deep Agents, LangChain, or LangGraph?",
            "reference" : "You should start with Deep Agents for a batteries-included agent with features like context compression and subagents, use LangChain's create_agent for a highly customizable agent harness, and use LangGraph, the low-level orchestration framework, for advanced workflows that combine deterministic and agentic steps."
        },
    {
            "question" : "How do you get structured output from a Pydantic schema?",
            "reference" : "For a standalone model, you call model.with_structured_output(MySchema), and for an agent, you pass the schema to the response_format parameter of create_agent, which validates the result and returns it in the structured_response key of the agent's state."
        },
    {
            "question" : "How do you give tools to a chat model?",
            "reference" : "You bind the tools with model.bind_tools([tool1, tool2]), and you then read the tool calls requested by the model from response.tool_calls, keeping in mind that outside of an agent you must execute the tools yourself."
        },
    {
            "question" : "How do you add conversational memory to an agent?",
            "reference" : "You specify a checkpointer, such as InMemorySaver from langgraph.checkpoint.memory, when creating the agent, and you pass {'configurable': {'thread_id': '1'}} as the config on each call, while in production you should use a database-backed checkpointer such as PostgresSaver."
        },
    {
            "question" : "How does the knowledge base tutorial load a PDF file?",
            "reference" : "The tutorial reads the PDF with the pypdf package, using pypdf.PdfReader to extract the text of each page, and it creates one Document per page with the source file and page number stored in the metadata."
        },
    {
            "question" : "How do you stream the tokens generated by an agent?",
            "reference" : "For new applications, the recommended approach is event streaming, introduced in LangChain v1.3, which you use by calling agent.stream_events(input, version='v3') and iterating over stream.messages and each message's .text, while the lower-level alternative is stream_mode='messages', which streams (token, metadata) tuples."
        }
]