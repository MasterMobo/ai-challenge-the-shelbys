import torch
import clip
from PIL import Image
from pathlib import Path

class KeyframeEmbedder:
    data_dir = './data/keyframes2'

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def embed_keyframes_from_folder(self):
        # Create paths from directory
        data_path = Path(self.data_dir)
        
        folder_paths = data_path.iterdir()
        
        keyframe_images = []
        # Process each folder
        for folder_path in folder_paths:
            print(f"Processing folder: {folder_path.name}")
            if folder_path.is_dir():
                print(f"Processing folder: {folder_path.name}")
                keyframe_paths = folder_path.iterdir()

                for keyframe_path in keyframe_paths:
                    
                    image = Image.open(keyframe_path)
                    keyframe_images.append(self.preprocess(image).to(self.device))

        print(f"Loaded {len(keyframe_images)} keyframes")

        # Stack images into a batch
        image_tensor = torch.stack(keyframe_images)

        # Generate embeddings
        with torch.no_grad():
            image_features = self.model.encode_image(image_tensor)

        # Save embeddings with the folder name
        output_path = Path(f'./out/{folder_path.name}.pt')
        self.save_embeddings(image_features, output_path)

    def save_embeddings(self, embeddings, output_path):
        torch.save(embeddings.cpu(), output_path)
        print(f"Embeddings saved to {output_path}")


if __name__ == "__main__":
    embedder = KeyframeEmbedder()
    embedder.embed_keyframes_from_folder()
