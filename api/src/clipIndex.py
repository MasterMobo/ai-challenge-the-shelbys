import numpy as np
import os
import torch
import clip
import pandas as pd
import config

class clipIndex:
    def __init__(self):
        pass

    def load_clip_indexes(self, combined_map_keyframe_file = config.combined_map_keyframe_file):
        return pd.read_csv(combined_map_keyframe_file)

    def look_up_clip_index(self, clip_index, combined_map_keyframe_file = config.combined_map_keyframe_file) -> pd.DataFrame:
        df = self.load_clip_indexes(combined_map_keyframe_file)
        result_frame = df[df['clip_index'] == clip_index] 
        return result_frame