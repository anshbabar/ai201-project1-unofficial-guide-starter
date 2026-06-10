from pathlib import Path
from typing import Any


def clean_text(text: str) -> str:
    """
    Remove unnecessary whitespace while preserving readable line breaks.
    """
    cleaned_lines = []

    for line in text.splitlines():
        # Remove leading/trailing whitespace and repeated spaces.
        cleaned_line = " ".join(line.split())

        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    return "\n".join(cleaned_lines)


def parse_document(source: str, text: str) -> dict[str, Any]:
    """
    Parse metadata, ratings, and review text from one cleaned review file.
    """
    metadata: dict[str, str] = {
        "source": source,
        "platform": "",
        "school": "",
        "source_url": "",
        "date_collected": "",
        "review_date": "",
        "overall_rating": "",
    }

    ratings: dict[str, str] = {}
    review_lines: list[str] = []

    current_section = "metadata"

    for line in text.splitlines():
        # Detect section changes.
        if line.startswith("Ratings"):
            current_section = "ratings"

            # Extract the overall rating when it appears on the Ratings line.
            if ":" in line:
                overall_rating = line.split(":", 1)[1].strip()
                metadata["overall_rating"] = overall_rating

            continue

        if line == "Review:":
            current_section = "review"
            continue

        # Parse the main metadata fields.
        if current_section == "metadata":
            if line.startswith("Source:"):
                metadata["platform"] = line.split(":", 1)[1].strip()

            elif line.startswith("School:"):
                metadata["school"] = line.split(":", 1)[1].strip()

            elif line.startswith("Source URL:"):
                metadata["source_url"] = line.split(":", 1)[1].strip()

            elif line.startswith("Date Collected:"):
                metadata["date_collected"] = line.split(":", 1)[1].strip()

            elif line.startswith("Review Date:"):
                metadata["review_date"] = line.split(":", 1)[1].strip()

        # Parse category ratings such as Food: 4 or Social: 2.
        elif current_section == "ratings":
            if ":" in line:
                category, value = line.split(":", 1)
                ratings[category.strip().lower()] = value.strip()

        # Store the actual student review.
        elif current_section == "review":
            review_lines.append(line)

    review_text = " ".join(review_lines).strip()

    if not review_text:
        raise ValueError(f"No review text found in {source}")

    return {
        "metadata": metadata,
        "ratings": ratings,
        "review_text": review_text,
    }


def load_documents(directory_path: str | Path) -> list[dict[str, Any]]:
    """
    Load, clean, and parse every .txt file in the provided directory.
    """
    directory = Path(directory_path)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    documents: list[dict[str, Any]] = []

    for file_path in sorted(directory.glob("*.txt")):
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            print(f"Skipping empty file: {file_path.name}")
            continue

        try:
            document = parse_document(
                source=file_path.name,
                text=cleaned_text,
            )
            documents.append(document)

        except ValueError as error:
            print(f"Skipping {file_path.name}: {error}")

    return documents


def create_chunks(documents):
    """
    Create one complete chunk for each student review.

    The searchable chunk includes the written review and category ratings
    so queries about topics such as food, clubs, or social life have more
    information available during semantic retrieval.
    """
    chunks = []

    for document in documents:
        metadata = document["metadata"]
        ratings = document["ratings"]
        review_text = document["review_text"]

        if not review_text.strip():
            continue

        source_stem = Path(metadata["source"]).stem

        ratings_text = ". ".join(
            f"{category.title()} rating: {value}"
            for category, value in ratings.items()
        )

        searchable_text = (
            f"Student review of UC San Diego. "
            f"{ratings_text}. "
            f"Written review: {review_text}"
        )

        chunk = {
            "id": f"{source_stem}_chunk_0",
            "text": searchable_text,
            "metadata": {
                **metadata,
                "ratings": ratings,
                "chunk_index": 0,
            },
        }

        chunks.append(chunk)

    return chunks



def print_chunk(chunk: dict[str, Any]) -> None:
    """
    Print one chunk in a readable format for manual inspection.
    """
    metadata = chunk["metadata"]

    print("\n" + "=" * 70)
    print(f"Chunk ID: {chunk['id']}")
    print(f"Source: {metadata['source']}")
    print(f"Review date: {metadata['review_date']}")
    print(f"Overall rating: {metadata['overall_rating']}")
    print(f"Chunk index: {metadata['chunk_index']}")
    print("-" * 70)
    print(chunk["text"])


if __name__ == "__main__":
    # Find the documents folder relative to this script.
    project_root = Path(__file__).resolve().parent
    documents_directory = project_root / "documents"

    # Stage 1: Load and parse the documents.
    documents = load_documents(documents_directory)

    print(f"Loaded {len(documents)} documents.")

    print("\nLoaded sources:")
    for document in documents:
        print(f"- {document['metadata']['source']}")

    # Stage 2: Create one chunk per review.
    chunks = create_chunks(documents)

    print(f"\nTotal chunks created: {len(chunks)}")

    # Stage 3: Print five representative chunks for inspection.
    print("\nFive sample chunks:")

    for chunk in chunks[:5]:
        print_chunk(chunk)

    if not chunks:
        print("No valid chunks were created.")

