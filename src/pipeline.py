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
    CROSS_ENCODER_THRESHOLD

)

from src.utils.logger import get_logger
logger = get_logger(__name__)


class RAGPipeline:
    def __init__(self):
        self.embedder = Embedder(EMBEDDING_MODEL)
        self.vectorstore = VectorStore(VECTORSTORE_PATH)
        self.llm = LLM()

    def build(self):
        """
        Build vectorstore from PDF (run once)
        """
        logger.info("Building vectorstore...")

        docs = load_pdf(PDF_PATH)
        chunker = TokenChunker()
        chunks = chunker.chunk_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
        logger.info("Embedding...")

        embeddings, metadata = self.embedder.embed_chunks(chunks)
        logger.info("Building index...")
        self.vectorstore.build(embeddings, metadata)
        self.vectorstore.save()

        self.retriever = Retriever(self.vectorstore, self.embedder)

        logger.info("Done — index saved.")
        logger.info(" Vectorstore built and saved!")

    def build_from_files(self, file_paths):
        """
        Build vectorstore from uploaded PDFs
        """
        logger.info(" Building from uploaded PDFs...")

        all_docs = []

        for path in file_paths:
            docs = load_pdf(path)
            all_docs.extend(docs)

        chunker = TokenChunker()
        chunks = chunker.chunk_documents(all_docs, CHUNK_SIZE, CHUNK_OVERLAP)

        logger.info("Embedding...")
        embeddings, metadata = self.embedder.embed_chunks(chunks)

        logger.info("Building index...")
        self.vectorstore.build(embeddings, metadata)

        # IMPORTANT: initialize retriever
        self.retriever = Retriever(self.vectorstore, self.embedder)

        logger.info(" Done building from uploaded files")


    def load(self):
        """
        Load existing vectorstore
        """
        logger.info("📂 Loading vectorstore...")
        self.vectorstore.load()
        logger.info(" Loaded!")
        # Initialize retriever AFTER loading
        self.retriever = Retriever(self.vectorstore, self.embedder)


    """
    Retrieve relevant chunks for a query
    """
    def query(self, question: str, top_k: int = 3):
    
        results = self.retriever.retrieve(question, top_k=top_k)
        logger.debug(f"Retrieved {len(results)} chunks before reranking")
        # results = sorted(results, key=lambda x: x["final_score"], reverse=True)
 
        """ OLD APPROACH:
             Used manual hybrid scoring (final_score) combining:
             - FAISS similarity
             - BM25 keyword score
             - word overlap
             This was heuristic and less accurate

             results = sorted(results, key=lambda x: x["final_score"], reverse=True)

             NEW APPROACH:
             Use cross-encoder score (deep semantic relevance)
             """
        results = sorted(results, key=lambda x: x.get("cross_score", 0), reverse=True)

        #HARD GUARD 1: no results 
        if not results:
            logger.warning("No results retrieved from retriever")
            return "No relevant context found.", []
        
        #HARD GUARD 2: weak relevance(most imp)
        # if results and results[0]["score"] < SCORE_THRESHOLD:       # OLD: sort using heuristic hybrid score (FAISS + BM25 + keyword overlap)
         
        # HARD GUARD 2 (use cross-encoder threshold ONLY)
        top_score = results[0].get("cross_score", 0)

        if top_score < CROSS_ENCODER_THRESHOLD:
            logger.warning(f"Top result below threshold: {top_score:.3f}")
            return "I don't know based on the provided document.", []
        
        # Filter bad chunks
        results = [r for r in results if r["cross_score"] > 0]
        logger.debug(f"{len(results)} chunks after cross_score filtering")

        # LLM call
        logger.info(f"Sending top {min(top_k, len(results))} chunks to LLM")

        answer = self.llm.generate(question, results[:top_k])

        logger.info("Answer generated successfully")

        return answer, results
    
        

    











    

