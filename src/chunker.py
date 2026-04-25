from transformers import AutoTokenizer

class TokenChunker:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)


    def chunk_documents(self, documents, chunk_size, overlap):
        """
        Args:
            documents: list of {"text", "page"} → keeps source info
            chunk_size: int → tokens per chunk (fits model limits)
            overlap: int → shared tokens (avoid context loss)

        Returns:
            list of {"text", "page", "chunk_index"} → for retrieval + tracing
        """

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        
        chunks = []

        for doc in documents:
            text = doc["text"]
            page = doc["page"]

            tokens = self.tokenizer.encode(text, add_special_tokens=False)

            start = 0
            chunk_index = 0

            while start < len(tokens):
                end = start + chunk_size
                chunk_tokens = tokens[start:end]

                chunk_text = self.tokenizer.decode(chunk_tokens)

                if len(chunk_tokens) < 20 and chunks:
                    chunks[-1]["text"] += " " + chunk_text
                    break

                chunks.append({
                    "text": chunk_text,
                    "page": page,
                    "chunk_index": chunk_index
                })

                start += chunk_size - overlap
                chunk_index += 1

        return chunks
        




















    

