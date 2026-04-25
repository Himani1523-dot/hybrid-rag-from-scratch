import numpy as np
from config import SCORE_THRESHOLD
from rank_bm25 import BM25Okapi

class Retriever:
    def __init__(self, vectorstore, embedder):
        self.vectorstore = vectorstore
        self.embedder = embedder
        
        print("[INIT] Building BM25 index...")        
        """
        BM25 setup (keyword-based retrieval)
        """
        self.tokenized_corpus = [
            chunk["text"].lower().split()
            for chunk in self.vectorstore.metadata
        ]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        print(f"[INIT] BM25 ready | Total chunks: {len(self.tokenized_corpus)}")


    def bm25_retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve chunks using BM25 (keyword search)
        WHY: - captures exact matches 
        """
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []
        for idx in top_indices:
            chunk_metadata = self.vectorstore.metadata[idx]
            print(f"[BM25] Score: {scores[idx]:.3f} | {chunk_metadata['text'][:50]}")

            results.append({
                **chunk_metadata,
                "bm25_score": float(scores[idx]),
                "global_idx": idx
            })

        return results


    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = SCORE_THRESHOLD): 

        """
        Retrieve top-k relevant chunks using cosine similarity (FAISS IP index)
        """
        top_k = max(1, top_k)   #prevents crash

        """ Step 1: Embed query (WITH normalization) """
        query_embedding = self.embedder.model.encode(
            [query],
            normalize_embeddings=True
        )[0]

        query_vector = np.array([query_embedding]).astype("float32")
        
        """ 
        Step 2 Semantic results (FAISS) and Keyword results (BM25)
        """
        faiss_scores, faiss_indices = self.vectorstore.index.search(query_vector, top_k)
        """          
        as BM25 needs more candidates improves hybrid quality so *2 
        """
        bm25_results = self.bm25_retrieve(query, top_k * 2)      

        results_dict = {}

        """ Add FAISS results"""
        for score, idx in zip(faiss_scores[0], faiss_indices[0]):

            if idx == -1:
                continue

            if score < score_threshold:
                continue

            chunk_metadata = self.vectorstore.metadata[idx]

            print(f"[FAISS] Score: {score:.3f} | {chunk_metadata['text'][:50]}")

            if len(chunk_metadata["text"].split()) < 40:
                continue

            results_dict[idx] = {
                **chunk_metadata,
                "score": float(score),
                "bm25_score": 0.0
            }

        """ Add BM25 results """
        for r in bm25_results:
            idx = r["global_idx"]   

            if idx in results_dict:
                results_dict[idx]["bm25_score"] = r["bm25_score"]
            else:
                results_dict[idx] = {
                    **r,
                    "score": 0.0,
                    "bm25_score": r["bm25_score"]
                }
        results = list(results_dict.values())

        if not results:
            return []

        results = self.rerank(query, results)
        return results


    def rerank(self, query, results):
        if not results:
            return []

        query_words = set(query.lower().split())

        for r in results:
            chunk_words = set(r["text"].lower().split())
            overlap = len(query_words & chunk_words)

            """ 
            Hybrid scoring results 
            """

            r["final_score"] = (
                0.6 * r.get("score", 0.0) +        # semantic
                0.3 * r.get("bm25_score", 0.0) +   # keyword
                0.1 * overlap                      # extra boost
            )

        results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    
        print("\n[FINAL TOP RESULTS]")
        for r in results[:3]:
            print(
                f"{r['final_score']:.3f} | "
                f"F:{r.get('score',0):.2f} | "
                f"B:{r.get('bm25_score',0):.2f} | "
                f"{r['text'][:50]}"
            )

        return results
    

    
    















        


        



    


    

    
