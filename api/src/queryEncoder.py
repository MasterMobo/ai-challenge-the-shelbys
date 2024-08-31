import torch
import numpy as np
import clip

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device, jit=False)

class queryEncoder:
    def __init__(self):
        pass
    
    def text_to_embedding(self, query):
        with torch.no_grad():
            text_tokens = clip.tokenize([query]).to(device)
            text_features = model.encode_text(text_tokens)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy()