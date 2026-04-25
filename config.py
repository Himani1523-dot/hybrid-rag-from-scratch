# Chunking settings (controls context size)
CHUNK_SIZE = 200
CHUNK_OVERLAP = 80

# Embedding model (can be changed based on performance needs)
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
Context control (prevents LLM overload)
"""
MAX_CHUNK_CHARS = 400
MAX_CONTEXT_CHARS = 1200

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



