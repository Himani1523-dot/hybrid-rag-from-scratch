""" vectorstore.py should only handle storage (build/save/load)
"""

import faiss
import numpy as np
import pickle
import os


class VectorStore:
    def __init__(self, path: str):
        self.path = path
        self.index = None
        self.metadata = None

    def build(self, embeddings,metadata):
        """
        Build FAISS index from provided embeddings + metadata
        """
        vectors = np.array(embeddings).astype("float32")

        dimension = vectors.shape[1]
        # self.index = faiss.IndexFlatL2(dimension)
        """faiss.IndexFlatIP(provides 100% accuracy) = used for finding the most similar vectors in high-dimensional datasets where accuracy is critical"""
        self.index = faiss.IndexFlatIP(dimension)         #This makes normalization actually work as cosine similarity
        self.index.add(vectors)
        self.metadata = metadata
    
    
    def save(self):
        """Save index and metadata to disk."""
        os.makedirs(self.path, exist_ok=True)             

        faiss.write_index(self.index, os.path.join(self.path, "index.faiss"))
        with open(os.path.join(self.path, "metadata.pkl"), "wb") as f:             #wb = write mode 
            pickle.dump(self.metadata, f)
            

    def load(self):
        """Load index and metadata from disk."""
        self.index = faiss.read_index(os.path.join(self.path, "index.faiss"))

        with open(os.path.join(self.path, "metadata.pkl"), "rb") as f:           #rb = read mode 
            self.metadata = pickle.load(f)

    def is_saved(self) -> bool:
        """Check if index already exists on disk."""
        return (os.path.exists(os.path.join(self.path, "index.faiss")) and
        os.path.exists(os.path.join(self.path, "metadata.pkl")))
    



    

    

    







    



















    



