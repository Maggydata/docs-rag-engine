from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from retrieval.vector_store import load_vector_store
from evaluation.questions import eval_questions
from rag.graph import build_rag_graph

from ragas import EvaluationDataset, evaluate
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import Faithfulness, ResponseRelevancy, LLMContextPrecisionWithReference, LLMContextRecall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

embedder = OpenAIEmbeddings(model = "text-embedding-3-small")
store = load_vector_store(embedder)
llm = ChatOpenAI(model = "gpt-4o-mini")
graph = build_rag_graph(store, llm, k=6)



samples = [] 
for i, item in enumerate(eval_questions):
    config = {"configurable" : {"thread_id": f"eval_{i}"}}
    result = graph.invoke({"messages" : [("user", item["question"])]}, config=config)
    samples.append(SingleTurnSample(
        user_input = item["question"],
        response = result["messages"][-1].content,
        retrieved_contexts = [c.page_content for c in result["retrieved_chunks"]],
        reference = item["reference"]
    ))
    
dataset = EvaluationDataset(samples = samples)


evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model = "gpt-4o-mini", temperature = 0))
evaluator_emb = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model = "text-embedding-3-small"))

metrics = [
    Faithfulness(llm = evaluator_llm),
    ResponseRelevancy(llm = evaluator_llm, embeddings = evaluator_emb),
    LLMContextPrecisionWithReference(llm = evaluator_llm),
    LLMContextRecall(llm = evaluator_llm)
]    

result = evaluate(dataset = dataset, metrics = metrics)
print(result)

df = result.to_pandas()
df.to_csv("eval_results.csv", index = False)