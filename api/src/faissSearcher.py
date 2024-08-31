import faiss
import queryEncoder
from config import *
import numpy as np

queryEncoder = queryEncoder.queryEncoder()
class faissSearcher:
    def __init__(self):
        pass
    
    def write_faiss_index(self, combined_clip_embeddings = np.load(combined_clip_file), destination = faiss_index_dir):
        d = combined_clip_embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(combined_clip_embeddings)
        faiss.write_index(index, destination)

    def read_faiss_index(self, faiss_index_dir=faiss_index_dir):
        return faiss.read_index(faiss_index_dir)

    def search_frames(self, query, top_k=5):
        faiss_index = self.read_faiss_index()
        text_embedding = query
        D, I = faiss_index.search(text_embedding, top_k)  # `D` is distances, `I` is indices of nearest neighbors
        return D, I