# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My project focuses on student experiences and perceptions of UC San Diego, especially academics and professional opportunities, social life, clubs, food, facilities, and campus location. The intended users are prospective students who want to understand what attending UCSD may feel like beyond official university descriptions.

This information is valuable because official websites explain programs and services, but they do not fully capture students’ everyday experiences. Student reviews provide useful perspectives on making friends, finding opportunities, joining clubs, campus culture, dining, and the overall environment, but these opinions are scattered across individual reviews and can be difficult to compare.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professor | A positive review highlighting UCSD’s scenery, opportunities, and the importance of joining clubs to make friends. | https://www.ratemyprofessors.com/school/1079 |
| 2 | Rate My Professor | A mixed review praising San Diego’s location while criticizing UCSD’s academic and social experience. | https://www.ratemyprofessors.com/school/1079 |
| 3 | Rate My Professor | A review describing UCSD as socially quiet but praising the surrounding area and professional opportunities. | https://www.ratemyprofessors.com/school/1079 |
| 4 | Rate My Professor | A negative review criticizing UCSD’s internet and social life while recognizing its location and internship opportunities. | https://www.ratemyprofessors.com/school/1079 |
| 5 | Rate My Professor | A positive review describing UCSD’s clubs, food, safety, location, and effort-based social life. | https://www.ratemyprofessors.com/school/1079 |
| 6 | Rate My Professor | A review praising UCSD’s academics, reputation, location, opportunities, and ability to find friends with similar interests. | https://www.ratemyprofessors.com/school/1079 |
| 7 | Rate My Professor | A review highlighting UCSD’s strong STEM opportunities while criticizing its food, social life, and school spirit. | https://www.ratemyprofessors.com/school/1079 |
| 8 | Rate My Professor | A review praising UCSD’s research and medical opportunities while noting weak social cohesion and limited gathering spaces. | https://www.ratemyprofessors.com/school/1079 |
| 9 | Rate My Professor | A positive review praising UCSD’s campus, supportive professors, and wide variety of student clubs. | https://www.ratemyprofessors.com/school/1079 |
| 10 | Rate My Professor | A highly positive review highlighting professional development, academics, clubs, food variety, and athletic facilities. | https://www.ratemyprofessors.com/school/1079 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** One complete student review per chunk, with a maximum size of approximately 700 words.

**Overlap:** No overlap for reviews that remain as one chunk. If a review exceeds the maximum length, it will be split at sentence boundaries with one sentence of overlap.

**Reasoning:** The documents are short Rate My Professors reviews that usually contain one student’s complete opinion about several related aspects of UCSD. Keeping each review together preserves its full meaning and prevents related sentences from being separated. A fixed maximum length is included only as a safeguard for unusually long reviews.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 through the sentence-transformers library. This model runs locally and will be used to embed the review chunks before storing them in ChromaDB.

**Top-k:** The system will retrieve the three most semantically relevant chunks for each query.

**Production tradeoff reflection:** For a production system, I would compare embedding models based on retrieval accuracy, latency, context length, multilingual support, privacy, and cost. A larger model might better understand detailed or domain-specific student language, but it could require more memory and produce slower responses. A multilingual model would be useful if the system included reviews written in languages other than English. I would also compare local models with API-based models based on whether improved retrieval quality would justify the additional cost and privacy concerns.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about academic and professional opportunities at UCSD? | Students generally describe opportunities as one of UCSD’s strengths, especially for STEM, research, medicine, internships, professional development, and learning. |
| 2 | Is it easy to make friends and have a social life at UCSD? | Opinions are mixed. Some students describe UCSD as socially quiet or reserved, while others say friendships can be developed by joining clubs, talking to classmates, and making an active effort. |
| 3 | What role do clubs play in student life at UCSD? | Students describe clubs as varied and important for meeting people, finding shared interests, and participating in campus activities. Clubs appear to be a major part of UCSD’s social life. |
| 4 | How do students describe the food at UCSD? | Opinions are mixed. Some students describe the food as decent, delicious, and varied, while others consider it one of the weaker parts of the UCSD experience. |
| 5 | What specific problems do students report about UCSD's internet quality and campus gathering spaces? | One student reports extremely unstable internet at Eighth College, including major latency spikes. Another student says UCSD lacks gathering spaces and social cohesion, although small groups can still thrive. The reviews provide limited evidence, so the answer should not make a campus-wide conclusion. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The dataset contains only 10 reviews, and some subjects are discussed much more frequently than others. Social life, opportunities, clubs, and location have strong coverage, while topics such as safety, internet quality, and facilities have limited written evidence. The system may need to refuse questions about topics that are not sufficiently covered.

2. The documents contain subjective and sometimes conflicting opinions. The retrieval system may return only strongly positive or strongly negative reviews, producing an unbalanced response. Retrieving four chunks should help the system compare multiple perspectives, but I will inspect the results and distance scores to verify their relevance.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

flowchart LR A[Rate My Professors Reviews<br>10 local TXT files] --> B[Document Ingestion<br>Python file loading and cleaning] B --> C[Review-Level Chunking<br>One review per chunk] C --> D[Embedding Model<br>all-MiniLM-L6-v2] D --> E[Vector Store<br>ChromaDB with source metadata] F[User Question] --> G[Semantic Retrieval<br>Top 4 relevant chunks] E --> G G --> H[Grounded Prompt<br>Retrieved context only] H --> I[Groq LLM<br>llama-3.3-70b-versatile] I --> J[Answer and Source List] J --> K[Gradio Query Interface]
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

     I will use Claude as a development assistant throughout the project by giving it the relevant sections of my planning.md, the assignment requirements, and examples of my document structure. I will ask it to help design code for loading and cleaning the 10 text files, keeping each review as one chunk, generating embeddings with all-MiniLM-L6-v2, storing them in ChromaDB with source metadata, retrieving the top four relevant chunks with distance scores, creating a grounded prompt for Groq’s llama-3.3-70b-versatile, adding source attribution, and connecting the pipeline to a Gradio interface. I will verify each output by reading the code, testing each stage separately, printing cleaned documents and chunks, checking stored metadata, manually reviewing retrieval results, testing supported and unsupported questions, and comparing all five system responses with the expected answers in my evaluation plan.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
