import torch
import clip
from PIL import Image
from pathlib import Path
import numpy as np
import os

class KeyframeEmbedder:
    data_dir = './out/keyframes'
    clip_embeddings_dir = './out/clip_embeddings'
    combined_clip_embedding_dir = './out/combined_clip_embedding.npy'

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

        self.data_path = Path(self.data_dir)
        self.clip_embeddings_path = Path(self.clip_embeddings_dir)

    def embedKeyframes(self):
        print(f"Embedding keyframes from {self.data_dir}")

        os.makedirs(self.clip_embeddings_dir, exist_ok=True)

        sorted_keyframe_folders = sorted(self.data_path.iterdir(), key=lambda x: self.keyframeFolderSortKey(x.stem))

        # Process each folder
        for keyframe_folder in sorted_keyframe_folders:
            print(f"Processing {keyframe_folder}")

            # Create paths from directory
            sorted_keyframe_paths = sorted(keyframe_folder.iterdir(), key=lambda x: self.keyframeFileSortKey(x.stem))

            # Load videos
            videos = [self.preprocess(Image.open(p)).unsqueeze(0).to(self.device) for p in sorted_keyframe_paths]

            # Stack them into a tensor and concatenate
            keyframe_images = torch.cat(videos, dim=0)

            print(f"Loaded {keyframe_images.size(0)} keyframes")

            # Generate embeddings
            with torch.no_grad():
                image_features = self.model.encode_image(keyframe_images)

            # Save embeddings with the folder name as a .npy file
            self.saveEmbeddings(image_features, keyframe_folder.stem)
        
        # Combine all the embeddings into a single numpy array
        self.combineEmbeddings()

    def saveEmbeddings(self, embeddings, video_name):
        # Convert the embeddings to numpy array
        embeddings_numpy = embeddings.cpu().numpy()
                
        # Save the numpy array
        output_path = os.path.join(self.clip_embeddings_dir, f"{video_name}.npy")
        np.save(output_path, embeddings_numpy)
        print(f"Embedding saved to {output_path}")

    def combineEmbeddings(self):
        # Combine all the embeddings into a single numpy array
        # Load all the embeddings
        print(f"Combining embeddings from {self.clip_embeddings_dir}")
        embeddings = []
        
        sorted_embeddings = sorted(self.clip_embeddings_path.iterdir(),
                                   key=lambda x: self.keyframeFolderSortKey(x.stem))

        for embedding_path in sorted_embeddings:
            embedding = np.load(embedding_path)
            embeddings.append(embedding)

        # Stack the embeddings into a single numpy array
        combined_embeddings = np.concatenate(embeddings, axis=0)

        # Save the combined embeddings
        np.save(self.combined_clip_embedding_dir, combined_embeddings)
        print(f"Combined embeddings saved to {self.combined_clip_embedding_dir}")

    def keyframeFolderSortKey(self, filename):
        parts = filename.split('_')
        level = int(parts[0][1:])  # Extracting number after 'L'
        video = int(parts[1][1:])  # Extracting number after 'V'
        return (level, video)

    # Define a function to extract the numeric parts from the filename
    def keyframeFileSortKey(self, filename):
        parts = filename.split('_')
        level = int(parts[0][1:])  # Extracting number after 'L'
        version = int(parts[1][1:])  # Extracting number after 'V'
        frame = int(parts[2])  # The frame number
        return (level, version, frame)

if __name__ == "__main__":
    embedder = KeyframeEmbedder()
    embedder.embedKeyframes()
