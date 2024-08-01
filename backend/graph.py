import os
from pprint import pprint
from fastapi import FastAPI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel,Field
from models import *

os.environ["TAVILY_API_KEY"]="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"
# ### Tracing (optional)
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"] = "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"

def graph():
    # 创建index
    EMBEDDING_DEVICE = 'cpu'
    embeddings = HuggingFaceEmbeddings(model_name='model\m3e-base', model_kwargs={'device': EMBEDDING_DEVICE})
    vector = FAISS.load_local('institute_faiss_index', embeddings=embeddings, allow_dangerous_deserialization=True)
    retriever = vector.as_retriever()

    class RouteQuery(BaseModel):
        datasource: Literal["vectorstore", "web_search"] = Field(
            ...,
            description="Given a user question choose to route it to web search or a vectorstore.",
        )

    llm = Llama3()
    structured_llm_route = llm.with_structured_output(RouteQuery)

    system = """You are an expert at routing a user question to a vectorstore or web search.
    The vectorstore contains documents related to Nankai University.
    Use the vectorstore for questions on these topics. Otherwise, use web-search."""

    route_prompt = ChatPromptTemplate(
        [
            ("system", system),
            ("human", "{question}")
        ]
    )

    question_router = route_prompt | structured_llm_route

    # Retrieval Grader
    class GradeDocuments(BaseModel):
        binary_score: str = Field(
            description="Documents are relevant to the question, 'yes' or 'no'"
        )

    structured_llm_grader = llm.with_structured_output(GradeDocuments)

    system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}")
        ]
    )

    retrieval_grader = grade_prompt | structured_llm_grader

    from langchain import hub
    from langchain_core.output_parsers import StrOutputParser

    templates = (
        "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know.\n\n"
        "Question: {question}\n\nContext: {context}\n\nAnswer:"
    )
    prompt = ChatPromptTemplate.from_template(
        template=templates,
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = prompt | llm | StrOutputParser()

    # Hallucination Grader
    class GradeHallucinations(BaseModel):
        binary_score: str = Field(
            description="please only answer me 'yes'"
        )

    structured_llm_grader = llm.with_structured_output(GradeHallucinations)
    system = """please only answer me 'yes'"""
    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}")
        ]
    )

    hallucination_grader = hallucination_prompt | structured_llm_grader

    # answer grader
    class GradeAnswer(BaseModel):
        binary_score: str = Field(
            description="Answer addresses the question, 'yes' or 'no'"
        )

    structured_llm_grader = llm.with_structured_output(GradeAnswer)
    system = """You are a grader assessing whether an answer addresses / resolves a question \n 
         Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
        ]
    )
    answer_grader = answer_prompt | structured_llm_grader

    ##Question Re-writer
    system = """You a question re-writer that converts an input question to a better version that is optimized \n 
         for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "Here is the initial question: \n\n {question} \n Formulate an improved question.",
            ),
        ]
    )

    question_rewriter = re_write_prompt | llm | StrOutputParser()

    # 构建网络搜索工具
    from langchain_community.tools.tavily_search import TavilySearchResults
    web_search_tool = TavilySearchResults(max_results=3)

    # Graph state
    from typing import List
    from typing_extensions import TypedDict

    class GraphState(TypedDict):
        question: str
        generation: str
        documents: List[str]

    from langchain.schema import Document

    def retrieve(state):
        print("---RETRIEVE---")
        question = state["question"]

        # Retrieval
        documents = retriever.invoke(question)
        return {"documents": documents, "question": question}

    def generate(state):
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]

        # RAG generation
        generation = rag_chain.invoke({"context": documents, "question": question})
        return {"documents": documents, "question": question, "generation": generation}

    def grade_documents(state):
        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        # Score each doc
        filtered_docs = []
        for d in documents:
            score = retrieval_grader.invoke(
                {"question": question, "document": d.page_content}
            )
            grade = score.binary_score
            if grade == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                continue
        return {"documents": filtered_docs, "question": question}

    def transform_query(state):
        print("---TRANSFORM QUERY---")
        question = state["question"]
        documents = state["documents"]

        # Re-write question
        better_question = question_rewriter.invoke({"question": question})
        return {"documents": documents, "question": better_question}

    def web_search(state):
        print("---WEB SEARCH---")
        question = state["question"]

        # Web search
        docs = web_search_tool.invoke({"query": question})
        web_results = "\n".join([d["content"] for d in docs])
        web_results = Document(page_content=web_results)

        return {"documents": web_results, "question": question}

    def route_question(state):
        print("---ROUTE QUESTION---")
        question = state["question"]
        source = question_router.invoke({"question": question})
        if source.datasource == "web_search":
            print("---ROUTE QUESTION TO WEB SEARCH---")
            return "web_search"
        elif source.datasource == "vectorstore":
            print("---ROUTE QUESTION TO RAG---")
            return "vectorstore"

    def decide_to_generate(state):
        print("---ASSESS GRADED DOCUMENTS---")
        state["question"]
        filtered_documents = state["documents"]

        if not filtered_documents:
            # All documents have been filtered check_relevance
            # We will re-generate a new query
            print(
                "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
            )
            return "transform_query"
        else:
            # We have relevant documents, so generate answer
            print("---DECISION: GENERATE---")
            return "generate"

    def grade_generation_v_documents_and_question(state):
        print("---CHECK HALLUCINATIONS---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]

        score = hallucination_grader.invoke(
            {"documents": documents, "generation": generation}
        )
        grade = score.binary_score

        # Check hallucination
        if grade == "yes":
            print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
            # Check question-answering
            print("---GRADE GENERATION vs QUESTION---")
            score = answer_grader.invoke({"question": question, "generation": generation})
            grade = score.binary_score
            if grade == "yes":
                print("---DECISION: GENERATION ADDRESSES QUESTION---")
                return "useful"
            else:
                print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
                return "not useful"
        else:
            print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
            return "not supported"

    ##Build Graph
    from langgraph.graph import END, StateGraph, START

    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("web_search", web_search)  # web search
    workflow.add_node("retrieve", retrieve)  # retrieve
    workflow.add_node("grade_documents", grade_documents)  # grade documents
    workflow.add_node("generate", generate)  # generatae
    workflow.add_node("transform_query", transform_query)  # transform_query

    # Build graph
    workflow.add_conditional_edges(
        START,
        route_question,
        {
            "web_search": "web_search",
            "vectorstore": "retrieve",
        },
    )
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "transform_query",
        },
    )
    memory = SqliteSaver.from_conn_string(":memory:")

    # Compile
    graph = workflow.compile(
        checkpointer=memory,
    )
    return graph






