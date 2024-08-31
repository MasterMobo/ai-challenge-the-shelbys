import faissSearcher
import numpy as np
import os
import torch
import clip
import config

class clipEmbedding:
    def __init__(self):
        pass

    
    def combine_clip_embeddings(self, clip_dir):
        clip_files = []
        for index in range(1, 32):
            file_number = str(index).zfill(3)
            filename = f"L01_V{file_number}.npy"
            clip_files.append(os.path.join(clip_dir, filename))

        # Initialize an empty list to store the features
        clip_embeddings = []

        # Loop through all .npy files in the directory
        for clip_file in clip_files:
            features = np.load(clip_file)
            clip_embeddings.append(features)

        # Concatenate all features into a single array
        clip_embeddings = np.concatenate(clip_embeddings)
        
        return clip_embeddings


# def save_clip_embeddings(clip_embeddings, destination):
#     np.save(destination, clip_embeddings)