import subprocess
import os, shutil
import csv
import pandas as pd
from pathlib import Path
import datetime import timdelta
import math

class KeyframeExtractor:
    data_dir = './data/videos'
    keyframe_output_dir = './out/keyframes'
    metadata_output_dir = './out/metadata'
    metadata_processed_dir = './out/metadata_processed.csv'

    def __init__(self, scene_threshold=0.3):
        self.scene_threshold = scene_threshold

        # Create paths from directory
        self.data_path = Path(self.data_dir)
        self.keyframe_output_path = Path(self.keyframe_output_dir)
        self.metadata_output_path = Path(self.metadata_output_dir)
        self.metadata_processed_path = Path(self.metadata_processed_dir)

        self.current_clip_index = 0

    def processVideos(self):
        # Iterate through each video to extract keyframes and metadata

        # Check if the output directories exist
        if self.keyframe_output_path.exists():
            print(f"Keyframe output directory already exists at {self.keyframe_output_path}.")
            print("Skipping shot detection.")
            return
        
        if self.metadata_output_path.exists():
            print(f"Metadata output directory already exists at {self.metadata_output_path}.")
            print("Skipping shot detection.")
            return

        # Create directories if they don't exist
        os.makedirs(self.keyframe_output_path, exist_ok=True)
        os.makedirs(self.metadata_output_path, exist_ok=True)
        
        self.current_clip_index = 0
        
        self.detectShots()
        self.extractShotData()
        self.getMiddleFrame()

        print(f"Shot detection completed. Keyframes saved at {self.keyframe_output_path}. Metadata saved at {self.metadata_output_path}.")

    def detectShots(self):
        # Detect shots in a video and save keyframes and metadata
        # Save keyframes (as PNG's) into out/keyframes
        # Save metadata into out/metadata
        folder_paths = self.data_path.iterdir()

        for folder_path in folder_paths:
            video_paths = folder_path.iterdir()

            for video_path in video_paths:
                print(f"Extracting keyframes from video: {video_path}")                    

                # Extract video name
                video_name = video_path.stem
                keyframes_save_path = os.path.join(self.keyframe_output_dir, video_name)

                os.makedirs(keyframes_save_path, exist_ok=True)

                # ffmpeg command to detect shots
                command = [
                    'ffmpeg',
                    '-i', video_path,
                    '-vf', f"select='eq(n\,0)+gt(scene,{self.scene_threshold})',showinfo",
                    '-vsync', 'vfr',
                    '-q:v', '2', 
                    '-frame_pts', 'true',
                    f'{keyframes_save_path}/{video_name}_%03d.png'
                ]
                
                # Save metadata
                metadata_file = os.path.join(self.metadata_output_path, f'{video_name}_metadata.txt')

                # Run ffmpeg command
                with open(metadata_file, 'w') as f:
                    subprocess.run(command, stderr=f)

    def getMiddleFrame(self):
        """
        This func will calculate the frame index i of the middle frame of a certain shot
        """
        metadata_processed_df = pd.read_csv(self.metadata_processed_path)
        for i in range(len(metadata_processed_df) - 1):

            cur_keyframe_index = metadata_processed_df.iloc[i]['frame_index']
            cur_keyframe_timestamp = metadata_processed_df.iloc[i]['timestamp']
            cur_keyframe_pts = metadata_processed_df.iloc[i]['pts_time']

            next_keyframe_index = metadata_processed_df.iloc[i+1]['frame_index']

            # then calculate the frame index based on the timestamp
            middle_frame_index = int((cur_keyframe_index + next_keyframe_index) // 2)
            middle_frame_pts = middle_frame_index / 25 #float
            # hh:mm:ss
            middle_frame_timedelta = timdelta(seconds=middle_frame_pts)
            middle_frame_timestamp = str(middle_frame_timedelta)
            
            # write result to mtdt csv 
            metadata_processed_df.at[i, 'middle_index'] = middle_frame_index
            metadata_processed_df.at[i, 'middle_timestamp'] = middle_frame_timestamp
            metadata_processed_df.at[i, 'middle_pts'] = middle_frame_pts

            # current iter if the last shot is reached
            if (next_keyframe_index < cur_keyframe_index):
                metadata_processed_df.at[i, 'middle_index'] = cur_keyframe_index
                metadata_processed_df.at[i, 'middle_timestamp'] = cur_keyframe_timestamp
                metadata_processed_df.at[i, 'middle_pts'] = cur_keyframe_pts

        # Handle the last shot
        metadata_processed_df.at[len(metadata_processed_df) - 1, 'middle_index'] = metadata_processed_df.iloc[-1]['frame_index']
        metadata_processed_df.at[len(metadata_processed_df) - 1, 'middle_timestamp'] = metadata_processed_df.iloc[-1]['timestamp']
        metadata_processed_df.at[len(metadata_processed_df) - 1, 'middle_pts'] = metadata_processed_df.iloc[-1]['pts_time']
        
        # convert middle_index to int
        metadata_processed_df['middle_index'] = metadata_processed_df['middle_index'].astype(int)

        # save to .csv
        metadata_processed_df.to_csv(self.metadata_processed_path, index=False)

    def extractShotData(self):
        # Read metadata files and write to human-readable csv
        
        # Write headers to csv file
        with open(self.metadata_processed_path, 'a', newline='') as out_f:
            csv_writer = csv.writer(out_f)
            csv_writer.writerow(['video_name', 'frame_index', 'timestamp', 'pts_time', 'clip_index'])
    
        sorted_keyframe_folders = sorted(self.keyframe_output_path.iterdir(),
                                        key=lambda x: self.keyframeFolderSortKey(x.stem))
        
        for keyframe_folder in sorted_keyframe_folders:
            video_name = keyframe_folder.stem
            metadata_file = os.path.join(self.metadata_output_path, f'{video_name}_metadata.txt')

            print(f"Processing metadata from file: {metadata_file}")                    

            # Sort based on keyframe's frame index number
            keyframe_images = sorted(keyframe_folder.iterdir(),
                                    key=lambda x: self.getFrameIndex(x.stem))
            
            # Read from metadata and write to .csv file
            with open(metadata_file, 'r') as f, open(self.metadata_processed_path, 'a', newline='') as out_f:
                csv_writer = csv.writer(out_f)                
                pts_time_arr = []

                # Find and append pts_time to pts_time_arr
                for line in f:
                    if 'pts_time' in line:
                        pts_time = float(line.split('pts_time:')[1].split(' ')[0])
                        pts_time_arr.append(pts_time)

                # Save to csv file
                for i, keyframe_file in enumerate(keyframe_images):
                    frame_index = self.getFrameIndex(keyframe_file.stem)
                    pts_time = pts_time_arr[i]
                    hours = int(pts_time // 3600)
                    minutes = int((pts_time % 3600) // 60)
                    seconds = pts_time % 60
                    timestamp = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
                    clip_index = self.current_clip_index

                    self.current_clip_index += 1

                    csv_writer.writerow([video_name, frame_index, timestamp, pts_time, clip_index])

    def keyframeFolderSortKey(self, filename):
        parts = filename.split('_')
        level = int(parts[0][1:])  # Extracting number after 'L'
        video = int(parts[1][1:])  # Extracting number after 'V'
        return (level, video)

    def getFrameIndex(self, videoName: str):
        return int(videoName.split("_")[-1])
            
if (__name__ == "__main__"):
    # Usage example
    detector = KeyframeExtractor(scene_threshold=0.3)
    detector.processVideos()
