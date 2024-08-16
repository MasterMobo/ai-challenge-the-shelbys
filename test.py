import faiss
import numpy as np
import os
import torch
import clip

# Directory containing the .npy files
feature_dir = "./data/clip-features-vit-b32-sample"
feature_files = [os.path.join(feature_dir, f) for f in os.listdir(feature_dir) if f.endswith(".npy")]

# Create a FAISS index
d = 512  # Dimensionality of CLIP features
index = faiss.IndexFlatL2(d)

frame_paths = []
current_index = 0

# Load and add features to the index
for feature_file in feature_files:
    print(f"Processing {feature_file}...")
    features = np.load(feature_file)
    
    # Optionally normalize features for cosine similarity
    # features = features / np.linalg.norm(features, axis=1, keepdims=True)
    
    # Add features to the index
    index.add(features)

    # Store the corresponding file and frame information
    num_frames = features.shape[0]
    video_name = os.path.basename(feature_file).replace(".npy", "")
    
    for i in range(num_frames):
        frame_paths.append((video_name, i))
    
    current_index += num_frames

# Save the index to disk for future use
faiss.write_index(index, "combined_faiss_index.index")



# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device, jit=False)

# Load the index
index = faiss.read_index("combined_faiss_index.index")

# Function to convert text query to an embedding using CLIP
def text_to_embedding(text):
    with torch.no_grad():
        text_tokens = clip.tokenize([text]).to(device)
        text_features = model.encode_text(text_tokens)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    return text_features.cpu().numpy()

# Function to perform a search in the FAISS index using the text embedding
def search_frames(query, top_k=5):
    text_embedding = text_to_embedding(query)
    D, I = index.search(text_embedding, top_k)  # `D` is distances, `I` is indices of nearest neighbors
    return D, I

# Sample search query
query = "Diver underwater hitting coral reef with hammer"

# Search for the top 5 frames that match the description
distances, result_indices = search_frames(query, top_k=5)

# Retrieve and display the results
for idx in result_indices[0]:
    video_name, frame_number = frame_paths[idx]
    print(f"Match: Video {video_name}, Frame {frame_number}, Distance: {distances[0][idx]}")