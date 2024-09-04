from keyframeExtractor import KeyframeExtractor
from embedKeyframes import KeyframeEmbedder
from queryEncoder import QueryEncoder
from faissSearcher import FAISSSearcher
from clipIndex import ClipIndexLookup
import time
import pandas as pd

class VideoSearcher:

    def __init__(self):
        # Extract keyframes from videos
        self.keyframeExtractor = KeyframeExtractor()
        self.keyframeExtractor.processVideos()

        # Embed keyframes
        self.keyframeEmbeder = KeyframeEmbedder()
        self.keyframeEmbeder.embedKeyframes()

        self.faissSearcher = FAISSSearcher() # Initialize the faiss searcher
        self.faissSearcher.write_faiss_index(self.keyframeEmbeder.combined_clip_embedding_dir) # Write the faiss index

        self.queryEncoder = QueryEncoder()  # Initialize the query encoder

        self.clipIndexLookup = ClipIndexLookup(self.keyframeExtractor.metadata_processed_dir)


    def search(self, query: str):
        # Start timer
        start_time = time.time()

        encoded_query = self.queryEncoder.textToEmbedding(query)  # Encode the query
        result_distances, result_indices = self.faissSearcher.search_frames(encoded_query, top_k=5)

        # End timer
        end_time = time.time()

        print(f"Search results for query: {query}")

        results = []

        # Retrieve and display the results
        for indexes in result_indices:
            for idx in indexes:
                result = self.clipIndexLookup.look_up_clip_index(idx)
                results.append(result)

        # Concatenate all result DataFrames into a single DataFrame
        combined_results = pd.concat(results, ignore_index=True)

        pd.set_option('display.max_columns', None)
        print(combined_results)
        pd.reset_option('display.max_columns')

        print(f"Search completed in {end_time - start_time:.2f} seconds")

        return combined_results





