import gradio as gr

from query import ask


def handle_query(question):
    """
    Run the RAG pipeline and format the output for the interface.
    """
    try:
        result = ask(question)

        sources = "\n".join(
            f"• {source}"
            for source in result["sources"]
        )

        return result["answer"], sources

    except Exception as error:
        return f"Error: {error}", ""


with gr.Blocks(title="The Unofficial UCSD Guide") as demo:
    gr.Markdown(
        """
        # The Unofficial UCSD Guide

        Ask questions about UCSD student experiences based on collected
        Rate My Professors school reviews.
        """
    )

    question_input = gr.Textbox(
        label="Your question",
        placeholder=(
            "Example: Is it easy to make friends and have a social life at UCSD?"
        ),
        lines=2,
    )

    ask_button = gr.Button("Ask")

    answer_output = gr.Textbox(
        label="Answer",
        lines=8,
    )

    sources_output = gr.Textbox(
        label="Retrieved sources",
        lines=4,
    )

    ask_button.click(
        fn=handle_query,
        inputs=question_input,
        outputs=[answer_output, sources_output],
    )

    question_input.submit(
        fn=handle_query,
        inputs=question_input,
        outputs=[answer_output, sources_output],
    )


if __name__ == "__main__":
    demo.launch()