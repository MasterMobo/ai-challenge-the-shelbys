import pandas as pd

class ClipIndexLookup:
    def __init__(self, metadata_processed_dir):
        self.df = pd.read_csv(metadata_processed_dir)
        pass

    def look_up_clip_index(self, clip_index) -> pd.DataFrame:
        result_frame = self.df[self.df['clip_index'] == clip_index] 
        return result_frame