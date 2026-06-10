# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This project covers student experiences and perceptions of the University of California San Diego. It focuses on topics that prospective students may want to understand before attending UCSD, including academic and professional opportunities, social life, clubs, food, facilities, and campus location.

This information is valuable because official university websites explain programs, services, and campus resources, but they do not fully describe what everyday student life feels like. Student opinions are spread across individual reviews, making it difficult for prospective students to compare different experiences or identify common patterns.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

All 10 documents were collected from the UC San Diego school page on Rate My Professors. Each document contains one student review, category ratings, a review date, and source metadata.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Review highlighting UCSD’s scenery, opportunities, and friendship-building through clubs | Student Review | documents/ucsd_review_01.txt |
| 2 | Mixed review praising San Diego while criticizing the academic and social experience | Student Review | documents/ucsd_review_02.txt |
| 3 | Review describing UCSD as socially quiet while praising the area and professional opportunities | Student Review | documents/ucsd_review_03.txt |
| 4 | Review criticizing internet quality and social life while praising internships and location | Student Review | documents/ucsd_review_04.txt |
| 5 | Review discussing clubs, food, safety, location, and effort-based social life | Student Review | documents/ucsd_review_05.txt |
| 6 | Review praising UCSD’s academics, reputation, location, opportunities, and friendships | Student Review | documents/ucsd_review_06.txt |
| 7 | Review praising STEM opportunities while criticizing food, social life, and school spirit | Student Review | documents/ucsd_review_07.txt |
| 8 | Review praising research and medical opportunities while noting limited gathering spaces | Student Review | documents/ucsd_review_08.txt |
| 9 | Review praising UCSD’s campus, supportive professors, and variety of clubs | Student Review | documents/ucsd_review_09.txt |
| 10 | Review praising professional development, academics, clubs, food variety, and athletic facilities | Student Review | documents/ucsd_review_10.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** One complete student review per chunk, with a maximum safeguard of approximately 700 words.

**Overlap:** No overlap was used for the current documents because every review remained within one chunk. If a future review exceeded the maximum length, it would be divided at sentence boundaries with one sentence of overlap.

**Why these choices fit your documents:** The documents are short student reviews rather than long articles or guides. Each review usually contains one student’s connected opinion about several aspects of UCSD. Keeping the complete review together preserves its meaning and prevents related statements from being divided across separate chunks. Before chunking, the pipeline removes repeated whitespace, ignores blank lines, parses important metadata, and separates the written review from its headings.

The searchable chunk also includes category ratings such as food, clubs, social life, and opportunities. This helps the embedding model associate each review with the topics it evaluates, although it can sometimes retrieve a review because of a rating even when the written text does not discuss that category in detail.

**Final chunk count:** 10 chunks from 10 documents.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 through the sentence-transformers library.

I selected this model because it runs locally, does not require an API key, produces relatively small 384-dimensional embeddings, and is fast enough for a small collection of English student reviews. The embeddings were normalized and stored in ChromaDB using cosine distance. The system retrieves the three most semantically relevant chunks for each query.

**Production tradeoff reflection:** For a production system, I would compare models based on retrieval accuracy, latency, context length, multilingual support, privacy, memory requirements, and cost. A larger embedding model might understand nuanced or domain-specific student language more accurately, but it could increase response time and infrastructure requirements. A multilingual model would be valuable if reviews were collected in several languages. I would also compare local and API-hosted models because an API model might improve accuracy while introducing recurring costs, network dependence, and privacy concerns.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The language model receives a system prompt with rules requiring it to:

Use only the student reviews supplied in the retrieved context.
Avoid using outside knowledge about UCSD.
Treat reviews as individual student opinions rather than universal facts.
Explain disagreements between reviews instead of presenting one opinion as the truth.
Respond with, “I don't have enough information in the collected reviews to answer that,” when the context does not contain sufficient evidence.
Avoid inventing statistics, programs, facilities, or student experiences.

Each retrieved chunk is placed in the prompt with a label such as:

[Source 1: ucsd_review_01.txt]
Review text...

The system uses Groq’s llama-3.3-70b-versatile model with a low temperature of 0.2 to reduce unnecessary creativity and keep responses focused on the evidence.

**How source attribution is surfaced in the response:** Source attribution is added programmatically after retrieval rather than depending entirely on the language model. The system collects the filename from the metadata of each retrieved chunk, removes duplicates, and displays the source filenames below the generated answer in the Gradio interface.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about academic and professional opportunities at UCSD? | Students generally describe opportunities as a major strength, especially for STEM, research, medicine, internships, professional development, and learning. | The response described UCSD as offering strong professional, research, and academic opportunities while noting that students may need to actively pursue them. | Relevant | Accurate |
| 2 | Is it easy to make friends and have a social life at UCSD? | Opinions are mixed. Some students describe UCSD as socially quiet, while others say friendships can be built through clubs, classes, and active effort. | The response explained that UCSD can feel reserved or socially quiet, but students can form friendships by joining clubs, speaking with classmates, and making an effort. | Relevant | Accurate |
| 3 | What role do clubs play in student life at UCSD? | Clubs are varied and important for meeting people, finding shared interests, and participating in social activities. | The response described clubs as an important way to find community, meet students with similar interests, and participate in social life outside Greek organizations. | Relevant | Accurate |
| 4 | How do students describe the food at UCSD? | Opinions are mixed. Some students describe the food as decent, varied, or delicious, while others consider it a weaker part of campus life. | The response presented both positive and negative food opinions, including praise for variety and criticism from students who rated food poorly. One retrieved review contained only a numeric food rating without a detailed written opinion. | Partially relevant | Partially accurate |
| 5 | What specific problems do students report about UCSD’s internet quality and campus gathering spaces? | One student reports unstable internet at Eighth College with major latency spikes. Another reports limited gathering spaces and weak social cohesion. The evidence is limited and should not be generalized to the entire campus. | The response identified at least one of the two reported issues, but it did not fully connect both the Eighth College internet complaint and the separate gathering-space complaint. | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What specific problems do students report about UCSD’s internet quality and campus gathering spaces?

**What the system returned:** The system returned a partially correct answer that discussed one of the requested topics more clearly than the other. It identified either the unstable internet complaint or the lack of gathering spaces, but it did not fully combine the evidence from both relevant reviews.

**Root cause (tied to a specific pipeline stage):** This was primarily a retrieval-stage failure. The question contains two separate semantic topics: internet quality and gathering spaces. The internet complaint appears in one review, while the gathering-space complaint appears in another. Because the system uses semantic similarity with top_k = 3, chunks strongly matching one half of the question can rank above the chunk needed for the other half. Category ratings can also influence retrieval even when the written review does not contain a detailed explanation of the topic.

**What you would change to fix it:** I would experiment with decomposing multi-part questions into separate retrieval queries and combining the results before generation. For this question, the system could search once for internet quality and once for gathering spaces, then merge and deduplicate the returned chunks. I could also test hybrid search using semantic similarity and keyword matching so specific terms such as “internet,” “latency,” and “gathering spaces” receive more weight.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The specification helped define each component before I wrote the pipeline. For example, deciding to treat each review as one chunk prevented me from using an arbitrary character split that would have separated short, connected student opinions. The retrieval plan also gave me a clear starting configuration using all-MiniLM-L6-v2, ChromaDB, and multiple retrieved perspectives.

**One way your implementation diverged from the spec, and why:** My original retrieval plan used top_k = 4, but I later changed it to top_k = 3. After considering the size of the dataset, I decided that retrieving four of only 10 reviews could introduce unrelated context. Three chunks still provide multiple perspectives while keeping the context more focused. I also added category ratings to the searchable chunk text after early tests showed that some topic queries, especially food, were not retrieving the expected reviews.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I gave Claude my document format, chunking strategy, and the requirement to load, clean, and process 10 Rate My Professors review files.
- *What it produced:* Claude helped produce an ingestion pipeline that loads .txt files, cleans whitespace, parses metadata and category ratings, extracts the written review, and creates one chunk per document.
- *What I changed or overrode:* I decided against a traditional fixed character split because the reviews were short and already represented complete thoughts. I kept each review as one chunk and used a maximum length only as a safeguard.

**Instance 2**

- *What I gave the AI:* I gave Claude my retrieval plan, including the all-MiniLM-L6-v2 embedding model, ChromaDB, my evaluation questions, and the early retrieval results.
- *What it produced:* Claude helped create the vector-store and retrieval code and suggested adding category ratings to the searchable text, using normalized embeddings, and configuring ChromaDB with cosine distance.
- *What I changed or overrode:* I changed the original top_k value from four to three because the dataset contains only 10 reviews and I wanted to reduce off-topic retrieval. I also manually inspected the returned chunks and kept the food retrieval issue as an honest failure rather than continuing to tune only for the evaluation questions.
