"""config.py"""
PDF_PATH = None

# Chunking settings (controls context size)
CHUNK_SIZE = 200
CHUNK_OVERLAP = 80

# Embedding model = bi-encoder model(can be changed based on performance needs)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Vector storage path
VECTORSTORE_PATH = "vectorstore/"


""" Retrieval settings
 We can tune retrieval depending on use case:
 - Higher TOP_K → more context (but may add noise)
 - Lower TOP_K → more precise answers
 - Higher threshold → stricter filtering (less hallucination)
 - Lower threshold → more recall (but risk of noise)
"""
TOP_K = 3

SCORE_THRESHOLD = 0.55  

"""
SCORE_THRESHOLD Used during FAISS (bi-encoder) retrieval stage to filter out low-similarity chunks.
Any chunk with cosine similarity below this threshold is discarded early. """    

"""
   Stage 1 → FAISS filter (SCORE_THRESHOLD)
   Stage 2 → Cross-encoder decision (CROSS_ENCODER_THRESHOLD)
   """
CROSS_ENCODER_THRESHOLD = 0.3

"""
Context control (prevents LLM overload)
"""
MAX_CHUNK_CHARS = 600
MAX_CONTEXT_CHARS = 1500

""" 
LLM configuration (flexible & replaceable)
 You can switch models depending on your use case:
 - Faster inference → smaller models (phi-3-mini, tinyllama)
 - Higher accuracy → larger models (mistral, llama3, GPT, etc.)
 - Production → API-based models (OpenAI, Claude, etc.)
 -  This design allows easy swapping without changing pipeline logic 
"""
LLM_BASE_URL = "http://localhost:1234/v1"
LLM_MODEL = "phi-3-mini"



