import os

from src.loader import load_pdf
from src.chunker import TokenChunker
from src.embedder import Embedder
from src.vectorstore import VectorStore
from src.retriever import Retriever
from src.llm import LLM

from config import (
    PDF_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    VECTORSTORE_PATH,
)

from config import SCORE_THRESHOLD

class RAGPipeline:
    def __init__(self):
        self.embedder = Embedder(EMBEDDING_MODEL)
        self.vectorstore = VectorStore(VECTORSTORE_PATH)
        # self.retriever = Retriever(self.vectorstore, self.embedder)
        self.llm = LLM()

    def build(self):
        """
        Build vectorstore from PDF (run once)
        """
        print("Building vectorstore...")

        docs = load_pdf(PDF_PATH)
        chunker = TokenChunker()
        chunks = chunker.chunk_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
        print("Embedding...")

        embeddings, metadata = self.embedder.embed_chunks(chunks)
        print("Building index...")
        self.vectorstore.build(embeddings, metadata)
        self.vectorstore.save()

        # Add 
        self.retriever = Retriever(self.vectorstore, self.embedder)

        print("Done — index saved.")
        print(" Vectorstore built and saved!")

    def build_from_files(self, file_paths):
        """
        Build vectorstore from uploaded PDFs
        """
        print("📂 Building from uploaded PDFs...")

        all_docs = []

        for path in file_paths:
            docs = load_pdf(path)
            all_docs.extend(docs)

        chunker = TokenChunker()
        chunks = chunker.chunk_documents(all_docs, CHUNK_SIZE, CHUNK_OVERLAP)

        print("Embedding...")
        embeddings, metadata = self.embedder.embed_chunks(chunks)

        print("Building index...")
        self.vectorstore.build(embeddings, metadata)

        # IMPORTANT: initialize retriever
        self.retriever = Retriever(self.vectorstore, self.embedder)

        print("✅ Done building from uploaded files")


    def load(self):
        """
        Load existing vectorstore
        """
        print("📂 Loading vectorstore...")
        self.vectorstore.load()
        print(" Loaded!")
        # Initialize retriever AFTER loading
        self.retriever = Retriever(self.vectorstore, self.embedder)

    def query(self, question: str, top_k: int = 3):
        """
        Retrieve relevant chunks for a query
        """
        results = self.retriever.retrieve(question, top_k=top_k)
        """
        Sort by similarity so best chunk is used first by LLM and guards
         WHY:
         - LLM pays more attention to earlier context
         - results[0] is used for threshold check
         - prevents good chunks from being ignored due to ordering
        """
        results = sorted(results, key=lambda x: x["final_score"], reverse=True)
        #HARD GUARD 1: no results 
        if not results:
            return "No relevant context found.", []
        #HARD GUARD 2: weak relevance(most imp)
        if results and results[0]["score"] < SCORE_THRESHOLD:
            return "I don't know based on the provided document.", []
        # LLM call
        answer = self.llm.generate(question, results)
        return answer ,results
    
        

    











    

