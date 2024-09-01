import faiss
import queryEncoder
from config import *
import numpy as np

queryEncoder = queryEncoder.QueryEncoder()
class FAISSSearcher:
    index_dir = "./out/faiss_index.index"

    def __init__(self):
        pass
    
    def write_faiss_index(self, combined_clip_embeddings_dir):
        combined_clip_embeddings = np.load(combined_clip_embeddings_dir)
        normalized_embeddings = self.normalize_embeddings(combined_clip_embeddings)

        d = normalized_embeddings.shape[1]
        index = faiss.IndexFlatIP(d)  # Use IndexFlatIP for cosine similarity
        index.add(normalized_embeddings)
        faiss.write_index(index, self.index_dir)

    def search_frames(self, query, top_k=5):
        faiss_index = self.read_faiss_index()
        text_embedding = self.normalize_embeddings(query)
        D, I = faiss_index.search(text_embedding, top_k)  # `D` is distances, `I` is indices of nearest neighbors
        return D, I

    def read_faiss_index(self):
        return faiss.read_index(self.index_dir)
    
    def normalize_embeddings(self, embeddings):
        return embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)


