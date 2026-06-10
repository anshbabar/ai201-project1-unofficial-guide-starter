import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from groq import Groq

from retrieval import load_embedding_model, retrieve_chunks


MODEL_NAME = "llama-3.3-70b-versatile"
COLLECTION_NAME = "ucsd_reviews"


def load_collection():
    """
    Connect to the existing persistent ChromaDB collection.
    """
    project_root = Path(__file__).resolve().parent
    database_directory = project_root / "chroma_db"

    client = chromadb.PersistentClient(path=str(database_directory))
    return client.get_collection(COLLECTION_NAME)


def build_context(retrieved_chunks):
    """
    Format retrieved reviews for the LLM prompt.
    """
    context_sections = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk["metadata"]["source"]
        text = chunk["text"]

        context_sections.append(
            f"[Source {index}: {source}]\n{text}"
        )

    return "\n\n".join(context_sections)


def generate_answer(question, retrieved_chunks, groq_client):
    """
    Generate an answer using only the retrieved review context.
    """
    context = build_context(retrieved_chunks)

    system_prompt = """
You are an assistant that answers questions about student experiences at
UC San Diego.

Follow these rules:
1. Use only the student reviews provided in the context.
2. Do not use outside knowledge about UCSD.
3. Treat the reviews as individual student opinions, not universal facts.
4. When reviews disagree, clearly summarize the different perspectives.
5. If the context does not contain enough information, say:
   "I don't have enough information in the collected reviews to answer that."
6. Do not invent facts, statistics, facilities, programs, or student experiences.
7. Keep the answer clear and concise.
"""

    user_prompt = f"""
Context:

{context}

Question:
{question}

Answer using only the context above.
"""

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
        max_tokens=400,
    )

    return response.choices[0].message.content.strip()


def ask(question):
    """
    Run the complete retrieval-augmented generation pipeline.
    """
    if not question or not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "retrieved_chunks": [],
        }

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found. Add it to your .env file."
        )

    groq_client = Groq(api_key=api_key)
    embedding_model = load_embedding_model()
    collection = load_collection()

    retrieved_chunks = retrieve_chunks(
        query=question,
        collection=collection,
        model=embedding_model,
        top_k=3,
    )

    answer = generate_answer(
        question=question,
        retrieved_chunks=retrieved_chunks,
        groq_client=groq_client,
    )

    # Add source attribution programmatically.
    sources = []

    for chunk in retrieved_chunks:
        source = chunk["metadata"]["source"]

        if source not in sources:
            sources.append(source)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


def print_result(question, result):
    """
    Print one complete answer for testing.
    """
    print("\n" + "=" * 80)
    print(f"Question: {question}")
    print("=" * 80)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source}")

    print("\nRetrieved chunks:")
    for rank, chunk in enumerate(result["retrieved_chunks"], start=1):
        print(
            f"{rank}. {chunk['metadata']['source']} "
            f"(distance: {chunk['distance']:.4f})"
        )


if __name__ == "__main__":
    test_question = (
        "Is it easy to make friends and have a social life at UCSD?"
    )

    result = ask(test_question)
    print_result(test_question, result)