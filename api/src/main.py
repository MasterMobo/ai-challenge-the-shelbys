import faissSearcher
import numpy as np
import os
import torch
import clip
import clipEmbedding
import clipIndex


# Load CLIP embeddings
clip_dir = "./data/clip-features-vit-b32-sample"

clip_embeddings = clipEmbedding.combine_clip_embeddings(clip_dir)
clipEmbedding.save_clip_embeddings(clip_embeddings, "./data/clip-embeddings.npy")

# Save CLIP indexes
keyframe_map_dir = './data/map-keyframes'
clip_index_destination = './data/clip-indexes.csv'

clipIndex.save_clip_indexes(keyframe_map_dir, clip_index_destination)

# Index FAISS
faiss_index_dir = './data/faiss-index'

faissSearcher.write_faiss_index(clip_embeddings, faiss_index_dir)
faiss_index = faissSearcher.read_faiss_index(faiss_index_dir)

# Search for similar frames
query = "Diver underwater hitting coral reef with hammer"
result_distances, result_indices = faissSearcher.search_frames(faiss_index, query, top_k=5)
print(result_indices)

# Retrieve and display the results
for indexes in result_indices:
    for idx in indexes:
        result = clipIndex.look_up_clip_index(clip_index_destination, idx)
        print(result)
