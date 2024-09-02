import numpy as np
from clipModel import CLIPModel

class QueryEncoder:
    def __init__(self):
        pass
    
    def textToEmbedding(self, query):
        with CLIPModel.torch.no_grad():
            text_tokens = CLIPModel.clip.tokenize([query]).to(device)
            text_features = CLIPModel.model.encode_text(text_tokens)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy()