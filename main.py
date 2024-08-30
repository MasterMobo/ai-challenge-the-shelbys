import faissSearcher
import numpy as np
import os
import torch
import clip
import clipIndex
import Mapper


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