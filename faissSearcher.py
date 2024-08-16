import faiss
import queryEncoder

def write_faiss_index(clip_embeddings, destination):
    d = clip_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(clip_embeddings)
    faiss.write_index(index, destination)

def read_faiss_index(faiss_index_dir):
    return faiss.read_index(faiss_index_dir)

def search_frames(faiss_index, query, top_k=5):
    text_embedding = queryEncoder.text_to_embedding(query)
    D, I = faiss_index.search(text_embedding, top_k)  # `D` is distances, `I` is indices of nearest neighbors
    return D, I