import numpy as np
import os
import torch
import clip
import pandas as pd

def save_clip_indexes(keyframe_map_dir, destination):
    # Initialize an empty list to store the DataFrames
    dataframes = []

    # Loop through all .csv files in the directory
    for index in range(1, 32):
        file_number = str(index).zfill(3)
        filename = f"L01_V{file_number}.csv"
        # Read the .csv file into a DataFrame
        df = pd.read_csv(os.path.join(keyframe_map_dir, filename))

        # Add video name as a new column
        df['video_name'] = os.path.splitext(filename)[0]

        # Append the DataFrame to the list
        dataframes.append(df)

    # Concatenate all DataFrames into a single DataFrame
    concatenated_df = pd.concat(dataframes, ignore_index=True)

    # Add a new column that counts from 0 to the end
    concatenated_df['clip_index'] = range(len(concatenated_df))



    # Save the concatenated DataFrame to a new .csv file (optional)
    concatenated_df.to_csv(destination, index=False)

def load_clip_indexes(clip_index_dir):
    return pd.read_csv(clip_index_dir)

def look_up_clip_index(clip_index_dir, clip_index):
    df = load_clip_indexes(clip_index_dir)
    result_frame = df[df['clip_index'] == clip_index] 
    return result_frame
