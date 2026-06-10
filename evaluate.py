from query import ask


EVALUATION_QUESTIONS = [
    {
        "question": (
            "What do students say about academic and professional "
            "opportunities at UCSD?"
        ),
        "expected_answer": (
            "Students generally describe opportunities as one of UCSD's "
            "strengths, especially for STEM, research, medicine, internships, "
            "professional development, and learning."
        ),
    },
    {
        "question": (
            "Is it easy to make friends and have a social life at UCSD?"
        ),
        "expected_answer": (
            "Opinions are mixed. Some students describe UCSD as socially "
            "quiet or reserved, while others say friendships can be developed "
            "through clubs, classmates, and active effort."
        ),
    },
    {
        "question": "What role do clubs play in student life at UCSD?",
        "expected_answer": (
            "Students generally describe clubs as varied and important for "
            "meeting people, finding shared interests, and participating in "
            "campus social activities."
        ),
    },
    {
        "question": "How do students describe the food at UCSD?",
        "expected_answer": (
            "Opinions are mixed. Some students describe the food as decent, "
            "delicious, and varied, while others consider it a weaker part "
            "of the UCSD experience."
        ),
    },
    {
        "question": (
            "What specific problems do students report about UCSD's "
            "internet quality and campus gathering spaces?"

        ),
        "expected_answer": (
            "One student reports extremely unstable internet at Eighth College, "
            "including major latency spikes. Another student says UCSD lacks "
            "gathering spaces and social cohesion, although small groups can "
            "still thrive. The reviews provide limited evidence, so the answer "
            "should not make a campus-wide conclusion."
        ),
    },
]


def print_evaluation_result(number, item, result):
    print("\n" + "=" * 90)
    print(f"Evaluation Question {number}")
    print("=" * 90)

    print(f"\nQuestion:\n{item['question']}")

    print(f"\nExpected answer:\n{item['expected_answer']}")

    print(f"\nSystem answer:\n{result['answer']}")

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
    for number, item in enumerate(EVALUATION_QUESTIONS, start=1):
        result = ask(item["question"])
        print_evaluation_result(number, item, result)