![Python](https://img.shields.io/badge/Python-3.12-blue)
![Framework](<https://img.shields.io/badge/Framework-None_(From_Scratch)-red>)
![RAG](https://img.shields.io/badge/RAG-Hybrid-green)
![LLM](https://img.shields.io/badge/LLM-Phi--3-orange)
![VectorDB](https://img.shields.io/badge/VectorDB-FAISS-purple)
![Retrieval](https://img.shields.io/badge/Retrieval-BM25+Semantic-yellow)
![UI](https://img.shields.io/badge/UI-Streamlit-ff4b4b)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Built From Scratch](https://img.shields.io/badge/Built-From%20Scratch-black)
![Status](https://img.shields.io/badge/Status-Active-success)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-blueviolet)

# Hybrid RAG Pipeline (From Scratch — No Frameworks)

A fully modular **Retrieval-Augmented Generation (RAG)** system built from scratch using Python — without relying on frameworks like LangChain or LlamaIndex.

This project demonstrates a **practical implementation of RAG systems**, focusing on retrieval quality, ranking strategies, and hallucination control.

---

## 🚨 What Makes This Different?

Unlike typical RAG projects that rely on frameworks, this system is:

- Built completely **from scratch**
- Designed with **full control over retrieval logic**
- Implements **hybrid search (FAISS + BM25)**
- Includes **custom reranking**
- Provides **debug visibility at every stage**

👉 The goal was not just to build RAG — but to understand _why it fails and how to fix it_

---

## 🚀 Overview

This project allows users to:

- Upload PDF documents
- Convert them into searchable knowledge
- Ask natural language questions
- Get answers grounded strictly in the document

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)**:

1. Retrieve relevant information from a knowledge base
2. Pass it to an LLM
3. Generate grounded answers

👉 Reduces hallucination and improves factual accuracy

---

## ⚙️ Architecture

```
PDF → Loader → Chunker → Embedder → Vector Store → Retriever → LLM → Answer
```

---

## 🔩 Components

### Loader

- Extracts text from PDFs (PyMuPDF)
- Cleans noisy content

---

### Token-Based Chunking

- Token-aware splitting with overlap

**Why?**

- Preserves semantic meaning
- Avoids context break

---

### Embeddings

- Model: `all-MiniLM-L6-v2`
- Normalized embeddings → cosine similarity via inner product

---

### Vector Store (FAISS)

- `IndexFlatIP`
- Fast semantic similarity search
- ⚠️ Vectorstore is not included. Run `pipeline.build()` to generate it.

---

### Hybrid Retrieval (Core Feature)

#### ❗ Problem

Semantic search alone can fail:

> High similarity ≠ correct answer

#### Solution

- **FAISS** → semantic meaning
- **BM25** → keyword matching
- **Merge + Rerank**

```
Final Score =
0.6 * semantic +
0.3 * bm25 +
0.1 * overlap
```

---

### 🧮 Reranking

Combines:

- semantic score
- keyword score
- token overlap

👉 Ensures best chunks reach LLM

---

### 🛡️ Guardrails

- ❌ No results → fallback response
- ❌ Low score → “I don’t know”
- ✅ Strict prompting (no hallucination)

---

### LLM (Flexible & Replaceable)

The system uses a local LLM (e.g., **Phi-3 via LM Studio**) for answer generation.

**Key Design Choice:**
The LLM layer is intentionally **modular and replaceable**, allowing easy upgrades based on project requirements.

---

###  Why this matters?

Different use cases require different models:

- ⚡ Fast responses → smaller models (Phi-3 Mini)
- 🧠 Higher accuracy → larger models (GPT-4, Claude, etc.)
- 🔒 Privacy → local models
- 🌐 Scalability → hosted APIs

---

###  Supported Options

This pipeline can be easily adapted to use:
Example: Switching from local model to OpenAI only requires updating config values.

- Local models (LM Studio, Ollama)
- OpenAI API (GPT models)
- Hugging Face models
- Any custom LLM endpoint

---

### 🌐 Streamlit UI

- Upload multiple PDFs
- Ask questions interactively
- View retrieved chunks (debug)

---

## ⚠️ Challenges & Fixes

### ❌ Semantic retrieval failure

FAISS ranked incorrect chunks higher

✅ Fixed with:

- BM25 integration
- Hybrid reranking

---

### ❌ Chunk ID collision

Same index across pages caused overwrites

✅ Fixed with:

- Global chunk indexing

---

### ❌ Hallucinated answers

LLM answered beyond context

✅ Fixed with:

- Score threshold guard
- Strict prompt
- Fallback response

---

### ❌ Initialization bug

BM25 failed due to missing metadata

✅ Fixed with:

- Proper pipeline ordering (load → retriever)

---

## 🧠 Design Philosophy

- Transparency over abstraction
- Control over convenience
- Understanding over shortcuts

Every component is manually implemented to expose real-world tradeoffs.

---

## 🔍 Example Query Flow

**Query:** _“What is Python?”_

1. FAISS → semantic chunks
2. BM25 → keyword chunks
3. Merge + rerank
4. Top chunks → LLM
5. LLM generates grounded answer

---

## 📂 Features

- ✅ Manual RAG pipeline
- ✅ Hybrid retrieval (FAISS + BM25)
- ✅ Token-based chunking
- ✅ Multi-document support
- ✅ Debug logs (FAISS / BM25 / Final scores)
- ✅ Guardrails against hallucination
- ✅ Local LLM integration

---

## 🔥 Future Improvements

- Cross-encoder reranker (BGE, etc.)
- Evaluation metrics (precision, recall)
- Improved BM25 preprocessing
- Streaming responses

---

## 🛠️ Tech Stack

- Python
- FAISS
- Sentence Transformers
- Rank-BM25
- PyMuPDF
- Streamlit
- LM Studio (Phi-3)

---

## 📌 Conclusion

This project demonstrates a **deep understanding of RAG systems**, including:

- Retrieval challenges
- Ranking strategies
- Context control
- LLM grounding

👉 Built entirely without frameworks to focus on core concepts.

---

⭐ If you found this useful, consider starring the repo!

## 📬 Contact

If you have any questions, feedback, or suggestions, feel free to reach out at **himani.sharma2315@gmail.com** — I’d be happy to connect!

