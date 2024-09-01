import numpy as np
import torch
import clip
import queryEncoder
import Mapper
from config import *
from chromaDBManager import ChromaDBManager
import time  # Import time to measure query duration

# Initialize ChromaDB manager
chromadb_manager = ChromaDBManager(collection_name="clip_embeddings")

# Load embeddings from the .npy file
embeddings = np.load('/app/combined_clip_embeddings.npy')

# Create metadata for each embedding 
metadata = [{'embedding_id': idx} for idx in range(len(embeddings))]

# Upload embeddings with metadata
chromadb_manager.upload_embeddings(embeddings, metadata)

# SEARCH QUERY GOES HERE!
query = "female reporter"

# Initialize the query encoder and encode the query
query_encoder = queryEncoder.queryEncoder()
encoded_query = query_encoder.text_to_embedding(query)

# Flatten the query embedding to ensure it is a flat list of floats
flat_encoded_query = [float(x) for sublist in encoded_query for x in sublist] if isinstance(encoded_query[0], (list, np.ndarray)) else [float(x) for x in encoded_query]

# Measure start time
start_time = time.time()

# Query the ChromaDB collection using the flattened text embedding
results = chromadb_manager.query_embeddings(flat_encoded_query, top_k=5)

# Measure end time and calculate query duration
end_time = time.time()
query_time = end_time - start_time
print(f"Query took {query_time:.4f} seconds")
print(results)

# # Print out the results including metadata
# for result in results['documents']:
#     print(f"ID: {result['id']}, Metadata: {result['metadata']}")
