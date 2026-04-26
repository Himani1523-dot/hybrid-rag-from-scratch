#bi-encoder model.
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_chunks(self, chunks, batch_size=32):
        """
        Batch embedding for better performance
        Returns:
            embeddings: List[List[float]]
            metadata: List[dict]
        """
        all_embeddings = []
        metadata = []

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            texts = [c["text"] for c in batch]

            embeddings = self.model.encode(
                texts,
                show_progress_bar=False,
                normalize_embeddings=True
            )                                     
            all_embeddings.extend(embeddings)

            # preserve metadata alignment
            for chunk in batch:
                metadata.append({
                    "text": chunk["text"],
                    "page": chunk.get("page"),
                    "chunk_index": chunk.get("chunk_index")
                })

        return all_embeddings, metadata


            
        
        
        
            







            



            







