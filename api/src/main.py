import faissSearcher
import numpy as np
import os
import torch
import clip
import clipIndex
import Mapper
import clipEmbedding
import config
import clipIndex

# Load CLIP embeddings
clip_dir = "./data/clip-features-vit-b32-sample"
clip_destination = "./out/clip-embeddings.npy"

clip_embeddings = clipEmbedding.combine_clip_embeddings(clip_dir)
clipEmbedding.save_clip_embeddings(clip_embeddings, clip_destination)

# Save CLIP indexes
keyframe_map_dir = './data/map-keyframes'
clip_index_destination = './out/clip-indexes.csv'

clipIndex = clipIndex.clipIndex()
clipIndex.look_up_clip_index(keyframe_map_dir, clip_index_destination)

# Index FAISS
faiss_index_dir = './out/faiss-index'

faissSearcher = faissSearcher.faissSearcher()
faissSearcher.write_faiss_index(clip_embeddings, faiss_index_dir)
faiss_index = faissSearcher.read_faiss_index(faiss_index_dir)

# Search for similar frames

# SEARCH QUERY GOES HERE!
query = "Diver underwater hitting coral reef with hammer"

result_distances, result_indices = faissSearcher.search_frames(query, top_k=5)
print(result_indices)

# Retrieve and display the results
for indexes in result_indices:
    for idx in indexes:
        result = clipIndex.look_up_clip_index(idx)
        print(result)
        frame_idx = result['frame_idx'].astype('int32')
        # timestamp = Mapper.frame_index_to_timestamp(frame_idx)
        # print(f"Frame index: {frame_idx}     Timestamp: {timestamp}")