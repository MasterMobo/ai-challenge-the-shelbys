from keyframeExtractor import KeyframeExtractor
from embedKeyframes import KeyframeEmbedder
from queryEncoder import QueryEncoder
from faissSearcher import FAISSSearcher
from clipIndex import ClipIndexLookup

class VideoSearcher:

    def search(self, query: str):
        # Extract keyframes from videos
        keyframeExtractor = KeyframeExtractor()
        keyframeExtractor.processVideos()

        # Embed keyframes
        keyframeEmbeder = KeyframeEmbedder()
        keyframeEmbeder.embedKeyframes()

        faissSearcher = FAISSSearcher() # Initialize the faiss searcher
        faissSearcher.write_faiss_index(keyframeEmbeder.output_dir) # Write the faiss index

        queryEncoder = QueryEncoder()  # Initialize the query encoder
        encoded_query = queryEncoder.textToEmbedding(query)  # Encode the query
        result_distances, result_indices = faissSearcher.search_frames(encoded_query, top_k=5)

        print(result_indices)

        clipIndexLookup = ClipIndexLookup()

        # Retrieve and display the results
        for indexes in result_indices:
            for idx in indexes:
                result = clipIndexLookup.look_up_clip_index(idx, keyframeExtractor.metadata_processed_dir)
                print(result)
                # frame_idx = result['frame_idx'].astype('int32')




