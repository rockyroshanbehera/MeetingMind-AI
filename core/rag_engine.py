import os

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from core.vector_store import (
    build_vector_store,
    load_vector_store,
    get_retriever
)


def get_llm():
    """
    Create the Mistral language model.
    """

    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3
    )


def format_docs(docs):
    """
    Format retrieved documents into context for the LLM.
    """

    formatted = []

    for doc in docs:

        chunk_index = doc.metadata.get(
            "chunk_index",
            "unknown"
        )

        formatted.append(
            f"[Source: Meeting Transcript | "
            f"Chunk {chunk_index}]\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(formatted)


def build_rag_chain(transcript: str):
    """
    Build a RAG pipeline for the current meeting.
    """

    vector_store = build_vector_store(transcript)

    retriever = get_retriever(
        vector_store,
        k=4
    )

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are MeetingMind, an AI meeting assistant.

Answer the user's question using ONLY the
meeting transcript context provided below.

Rules:

1. Do not invent information.
2. If the answer is not present in the context,
   say:
   "I could not find this information in the meeting transcript."
3. Keep answers concise and precise.
4. When possible, mention the relevant source
   chunk in your answer.
5. Distinguish clearly between facts and
   unresolved discussion.

Meeting transcript context:

{context}
"""
            ),
            (
                "human",
                "{question}"
            )
        ]
    )

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def load_rag_chain():
    """
    Load an existing vector store and create
    the RAG chain.
    """

    vector_store = load_vector_store()

    retriever = get_retriever(
        vector_store,
        k=4
    )

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are MeetingMind, an AI meeting assistant.

Answer the user's question using ONLY the
meeting transcript context provided below.

If the answer is not found in the context,
say:

"I could not find this information in the meeting transcript."

Be concise and precise.

Meeting transcript context:

{context}
"""
            ),
            (
                "human",
                "{question}"
            )
        ]
    )

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(
    rag_chain,
    question: str
) -> str:
    """
    Ask a question against the meeting RAG chain.
    """

    print(f"Question: {question}")

    answer = rag_chain.invoke(question)

    print(f"Answer: {answer}")

    return answer