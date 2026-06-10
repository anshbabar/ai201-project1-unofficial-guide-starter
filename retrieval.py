from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import create_chunks, load_documents


def load_chunks():
    """
    Load the review documents and convert them into searchable chunks.
    """
    project_root = Path(__file__).resolve().parent
    documents_directory = project_root / "documents"

    documents = load_documents(documents_directory)
    return create_chunks(documents)


def load_embedding_model():
    """
    Load the local sentence-transformers embedding model.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


def flatten_metadata(chunk):
    """
    Convert chunk metadata into simple values that ChromaDB can store.
    """
    metadata = chunk["metadata"]

    return {
        "source": metadata["source"],
        "platform": metadata["platform"],
        "school": metadata["school"],
        "source_url": metadata["source_url"],
        "date_collected": metadata["date_collected"],
        "review_date": metadata["review_date"],
        "overall_rating": metadata["overall_rating"],
        "chunk_index": metadata["chunk_index"],
    }


def create_vector_store(chunks, model):
    """
    Embed all chunks and store them in a persistent ChromaDB collection.
    """
    project_root = Path(__file__).resolve().parent
    database_directory = project_root / "chroma_db"

    client = chromadb.PersistentClient(path=str(database_directory))

    # Delete the existing collection so new embeddings replace old ones.
    try:
        client.delete_collection("ucsd_reviews")
    except Exception:
        pass

    collection = client.create_collection(
        name="ucsd_reviews",
        metadata={
            "description": "Student reviews about UC San Diego",
            "hnsw:space": "cosine",
        },
    )

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    ).tolist()

    ids = [chunk["id"] for chunk in chunks]
    metadatas = [flatten_metadata(chunk) for chunk in chunks]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return collection


def retrieve_chunks(query, collection, model, top_k=3):
    """
    Retrieve the three most semantically relevant chunks for a query.
    """
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    for index in range(len(results["ids"][0])):
        retrieved_chunks.append(
            {
                "id": results["ids"][0][index],
                "text": results["documents"][0][index],
                "metadata": results["metadatas"][0][index],
                "distance": results["distances"][0][index],
            }
        )

    return retrieved_chunks


def print_results(query, results):
    """
    Print retrieval results in a readable format.
    """
    print("\n" + "#" * 80)
    print(f"Query: {query}")
    print("#" * 80)

    for rank, result in enumerate(results, start=1):
        print("\n" + "=" * 70)
        print(f"Rank: {rank}")
        print(f"Source: {result['metadata']['source']}")
        print(f"Distance: {result['distance']:.4f}")
        print("-" * 70)
        print(result["text"])


if __name__ == "__main__":
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks.")

    model = load_embedding_model()
    print("Embedding model loaded.")

    collection = create_vector_store(chunks, model)

    print("Chunks stored successfully in ChromaDB.")
    print(f"Total items in collection: {collection.count()}")

    test_queries = [
        (
            "What do student reviews say about social life, friendship, "
            "and making friends at UCSD?"
        ),
        (
            "What do student reviews say about internships, research, jobs, "
            "and professional opportunities at UCSD?"
        ),
        (
            "What positive and negative opinions do student reviews give "
            "about UCSD food and dining?"
        ),
    ]

    for query in test_queries:
        results = retrieve_chunks(
            query=query,
            collection=collection,
            model=model,
            top_k=3,
        )

        print_results(query, results)