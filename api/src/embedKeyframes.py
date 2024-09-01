import torch
import clip
from PIL import Image
from pathlib import Path
import numpy as np

class KeyframeEmbedder:
    data_dir = './out/keyframes'
    output_dir = './out/clip_embedding.npy'

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def embedKeyframes(self):
        print(f"Embedding keyframes from {self.data_dir}")

        # Create paths from directory
        data_paths = sorted(Path(self.data_dir).iterdir(), key=lambda x: self.sortKey(x.name))

        # Load videos within the folder
        videos = [self.preprocess(Image.open(p)).unsqueeze(0).to(self.device) for p in data_paths]

        # Stack them into a tensor and concatenate
        keyframe_images = torch.cat(videos, dim=0)

        print(f"Loaded {keyframe_images.size(0)} keyframes")

        # Generate embeddings
        with torch.no_grad():
            image_features = self.model.encode_image(keyframe_images)

        # Save embeddings with the folder name as a .npy file
        self.saveEmbeddings(image_features)

    def saveEmbeddings(self, embeddings):
        # Convert the embeddings to numpy array
        embeddings_numpy = embeddings.cpu().numpy()
                
        # Save the numpy array
        output_path = Path(self.output_dir)
        np.save(output_path, embeddings_numpy)
        print(f"Embeddings saved to {output_path}")

    # Define a function to extract the numeric parts from the filename
    def sortKey(self, filename):
        parts = filename.split('.')[0].split('_')
        level = int(parts[0][1:])  # Extracting number after 'L'
        version = int(parts[1][1:])  # Extracting number after 'V'
        frame = int(parts[2])  # The frame number
        return (level, version, frame)

if __name__ == "__main__":
    embedder = KeyframeEmbedder()
    embedder.embedKeyframes()
