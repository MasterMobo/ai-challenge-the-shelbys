import numpy as np
from chromadb import Client


class ChromaDBManager:
    def __init__(self, collection_name="clip_embeddings"):
        self.client = Client()  # Initialize the ChromaDB client
        self.collection_name = collection_name
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self):
        try:
            # Try to get the collection if it exists
            collection = self.client.get_collection(self.collection_name)
        except ValueError:
            # If the collection doesn't exist, create a new one
            collection = self.client.create_collection(name=self.collection_name)
        return collection

    def upload_embeddings(self, embeddings, metadata):
        """
        Uploads embeddings to ChromaDB with associated metadata.

        :param embeddings: List of embeddings.
        :param metadata: List of dictionaries containing metadata (e.g., {'video_id': 'video1', 'frame_index': 5}).
        """
        ids = [str(idx) for idx in range(len(embeddings))]

        # Use flatten_embedding to ensure each embedding is a flat list of floats
        vectors = [self.flatten_embedding(embedding) for embedding in embeddings]

        # Define the maximum batch size allowed by ChromaDB
        max_batch_size = 41666

        # Split embeddings and metadata into smaller batches and upload them
        for i in range(0, len(vectors), max_batch_size):
            batch_ids = ids[i:i + max_batch_size]
            batch_vectors = vectors[i:i + max_batch_size]
            batch_metadata = metadata[i:i + max_batch_size]

            # Upload the current batch to ChromaDB with metadata
            self.collection.add(ids=batch_ids, embeddings=batch_vectors, metadatas=batch_metadata)

    def flatten_embedding(self, embedding):
        """Flatten embedding and ensure it is a list of floats."""
        # If the embedding is already a flat list, convert its elements to floats
        if isinstance(embedding[0], (int, float)):
            return [float(x) for x in embedding]
        # If the embedding is a nested list, flatten it and convert to float
        else:
            return [float(x) for sublist in embedding for x in sublist]

    def query_embeddings(self, query_embedding, top_k=5):
        # Perform the query and return the results
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        return results

    def __init__(self, collection_name="clip_embeddings"):
        self.client = Client()  # Initialize the ChromaDB client
        self.collection_name = collection_name
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self):
        try:
            # Try to get the collection if it exists
            collection = self.client.get_collection(self.collection_name)
        except ValueError:
            # If the collection doesn't exist, create a new one
            collection = self.client.create_collection(name=self.collection_name)
        return collection

    def upload_embeddings(self, embeddings, metadata):
        """
        Uploads embeddings to ChromaDB with associated metadata.

        :param embeddings: List of embeddings.
        :param metadata: List of dictionaries containing metadata (e.g., {'video_id': 'video1', 'frame_index': 5}).
        """
        ids = [str(idx) for idx in range(len(embeddings))]

        # Convert each embedding to a list of floats
        vectors = [embedding.tolist() for embedding in embeddings]

        # Define the maximum batch size allowed by ChromaDB
        max_batch_size = 41666

        # Split embeddings and metadata into smaller batches and upload them
        for i in range(0, len(vectors), max_batch_size):
            batch_ids = ids[i:i + max_batch_size]
            batch_vectors = vectors[i:i + max_batch_size]
            batch_metadata = metadata[i:i + max_batch_size]

            # Upload the current batch to ChromaDB with metadata
            self.collection.add(ids=batch_ids, embeddings=batch_vectors, metadatas=batch_metadata)

    def query_embeddings(self, query_embedding, top_k=5):
        # Query the ChromaDB collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results
