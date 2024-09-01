import faissSearcher
import numpy as np
import os
import torch
import clip
import clipIndex
import queryEncoder
import Mapper
from config import *

# SEARCH QUERY GOES HERE!
query = "female reporter"

queryEncoder = queryEncoder.queryEncoder()  # Initialize the query encoder
encoded_query = queryEncoder.text_to_embedding(query)  # Encode the query

faissSearcher = faissSearcher.faissSearcher() # Initialize the faiss searcher
clipIndex = clipIndex.clipIndex() # Initialize the clip index
    
faissSearcher.write_faiss_index() # Write the faiss index
result_distances, result_indices = faissSearcher.search_frames(encoded_query, top_k=5)

print(result_indices)

# Retrieve and display the results
for indexes in result_indices:
    for idx in indexes:
        result = clipIndex.look_up_clip_index(idx)
        print(result)
        frame_idx = result['frame_idx'].astype('int32')
        # timestamp = Mapper.frame_index_to_timestamp(frame_idx)
        # print(f"Frame index: {frame_idx}     Timestamp: {timestamp}")