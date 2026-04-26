### RAG Upgrade: From Heuristic Reranking → Cross-Encoder

#### Previous Approach (Before Change)

Earlier, the system used a **manual hybrid scoring function** for ranking retrieved chunks:

```python
final_score = (
    0.6 * semantic_score (FAISS)
  + 0.3 * bm25_score
  + 0.1 * keyword_overlap
)
```

#### Problems with This Approach

- Scores were **manually tuned weights** → not learned
- FAISS similarity only compares vectors → **no deep understanding**
- Keyword overlap is shallow → fails on paraphrased queries
- BM25 helps but still **surface-level matching**
- Ranking quality degraded when:
  - query is complex
  - wording differs from document

- Result:
  - sometimes wrong chunks ranked higher
  - LLM received weaker context
  - increased hallucination risk

👉 In short: ranking logic was **heuristic, not intelligent**

---

#### New Approach (After Change)

Replaced manual reranking with a **Cross-Encoder model**:

```python
(query, chunk) → CrossEncoder → relevance score
```

Model used:

```python
cross-encoder/ms-marco-MiniLM-L-6-v2
```

---

#### What Changed

**1. retriever.py**

- Added Cross-Encoder initialization
- Added `cross_rerank()` method
- Replaced:

  ```python
  rerank() → cross_rerank()
  ```

---

**2. pipeline.py**

- Sorting updated:

  ```python
  final_score ❌ → cross_score ✅
  ```

- Relevance guard updated:

  ```python
  FAISS score ❌ → cross_score ✅
  ```

---

**3. config.py**

- Introduced:

  ```python
  CROSS_ENCODER_THRESHOLD
  ```

- Reason:
  - Cross-encoder scores have different scale than cosine similarity

---

#### 🧠 Why Cross-Encoder is Better

**Key difference:**

| Bi-Encoder (Before) | Cross-Encoder (Now)     |
| ------------------- | ----------------------- |
| Encodes separately  | Evaluates together      |
| Fast but shallow    | Slower but accurate     |
| Vector similarity   | True semantic relevance |

👉 Cross-encoder actually reads:

```text
Query + Chunk → understands relationship
```

Instead of just comparing embeddings.

---

#### Impact of This Change

- Better ranking of relevant chunks
- More accurate context sent to LLM
- Reduced hallucinations
- Handles:
  - paraphrased queries
  - long/complex questions
  - semantic meaning (not just keywords)

---

#### ⚙️ Updated Pipeline Flow

```text
Query
 ↓
Bi-Encoder (FAISS) + BM25  → candidate retrieval
 ↓
🔥 Cross-Encoder → reranking (main decision layer)
 ↓
Top chunks
 ↓
LLM
```

---

#### 📌 Key Design Decision

After introducing cross-encoder:

- FAISS score is used only for **retrieval filtering**
- Cross-encoder score is used for:
  - ranking
  - threshold filtering (final decision)

---

#### 🧠 Core Insight

This change shifts the system from:

👉 "similar vectors = relevant"

to

👉 "model understands query + text = relevant"

---

#### 🚀 Result

System moved from:

- heuristic ranking

to:

- **learned semantic ranking**

This significantly improves real-world RAG performance and reliability.

---
