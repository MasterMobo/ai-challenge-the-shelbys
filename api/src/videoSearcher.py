from keyframeExtractor import KeyframeExtractor
from embedKeyframes import KeyframeEmbedder
from queryEncoder import QueryEncoder
from faissSearcher import FAISSSearcher
from clipIndex import ClipIndexLookup
import time
class VideoSearcher:

    def search(self, query: str):
        # Start timer
        start_time = time.time()

        # Extract keyframes from videos
        keyframeExtractor = KeyframeExtractor()
        keyframeExtractor.processVideos()

        # Embed keyframes
        keyframeEmbeder = KeyframeEmbedder()
        keyframeEmbeder.embedKeyframes()

        faissSearcher = FAISSSearcher() # Initialize the faiss searcher
        faissSearcher.write_faiss_index(keyframeEmbeder.combined_clip_embedding_dir) # Write the faiss index

        queryEncoder = QueryEncoder()  # Initialize the query encoder
        encoded_query = queryEncoder.textToEmbedding(query)  # Encode the query
        result_distances, result_indices = faissSearcher.search_frames(encoded_query, top_k=5)

        # End timer
        end_time = time.time()

        print(f"Search results for query: {query}")

        clipIndexLookup = ClipIndexLookup()

        # Retrieve and display the results
        for indexes in result_indices:
            for idx in indexes:
                result = clipIndexLookup.look_up_clip_index(idx, keyframeExtractor.metadata_processed_dir)
                print(result)
                # frame_idx = result['frame_idx'].astype('int32')

        print(f"Search completed in {end_time - start_time:.2f} seconds")





