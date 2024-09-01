import torch
import clip
from PIL import Image
from pathlib import Path
import numpy as np

class KeyframeEmbedder:
    data_dir = './data/keyframes2'

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def embed_keyframes_from_folder(self):
        # Create paths from directory
        data_path = Path(self.data_dir)
        
        folder_paths = data_path.iterdir()
        
        keyframe_images = None
        # Process each folder
        for folder_path in folder_paths:
            print(f"Processing folder: {folder_path.name}")
            if folder_path.is_dir():
                keyframe_paths = list(folder_path.iterdir())

                # Process keyframes within the folder
                folder_images = [self.preprocess(Image.open(p)).unsqueeze(0).to(self.device) for p in keyframe_paths]

                # Stack them into a tensor and concatenate
                folder_tensor = torch.cat(folder_images, dim=0)
                
                if keyframe_images is None:
                    keyframe_images = folder_tensor
                else:
                    keyframe_images = torch.cat((keyframe_images, folder_tensor), dim=0)

        if keyframe_images is None:
            print("No keyframes found.")
            return None, None

        print(f"Loaded {keyframe_images.size(0)} keyframes")

        # Generate embeddings
        with torch.no_grad():
            image_features = self.model.encode_image(keyframe_images)

        # Save embeddings with the folder name as a .npy file
        output_path = Path(f'./out/{folder_path.name}.npy')
        self.save_embeddings(image_features, output_path)

    def save_embeddings(self, embeddings, output_path):
        # Convert the embeddings to numpy array
        embeddings_numpy = embeddings.cpu().numpy()
        
        # Print the shape of the numpy array
        print(f"Shape of the embeddings: {embeddings_numpy.shape}")
        
        # Save the numpy array
        np.save(output_path, embeddings_numpy)
        print(f"Embeddings saved to {output_path}")


if __name__ == "__main__":
    embedder = KeyframeEmbedder()
    embedder.embed_keyframes_from_folder()
