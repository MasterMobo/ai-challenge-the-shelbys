import subprocess
import os
import csv
from pathlib import Path

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

        # Create directories if they don't exist
        os.makedirs(self.keyframe_output_path, exist_ok=True)
        os.makedirs(self.metadata_output_path, exist_ok=True)

        folder_paths = self.data_path.iterdir()

        with open(self.metadata_processed_path, 'a', newline='') as out_f:
            csv_writer = csv.writer(out_f)
            #  Headers
            csv_writer.writerow(['video_name', 'frame_index', 'timestamp', 'pts_time', 'clip_index'])
        
        # Process each folder
        for folder_path in folder_paths:
            if not folder_path.is_dir():
                continue

            video_paths = folder_path.iterdir()

            for video_path in video_paths:
                self.detectShots(video_path)
                self.extractShotData(video_path)
        
        self.current_clip_index = 0

        print(f"Shot detection completed. Keyframes saved at {self.keyframe_output_path}. Metadata saved at {self.metadata_output_path}.")

    def detectShots(self, video_path):
        # Detect shots in a video and save keyframes and metadata
        # Save keyframes (as PNG's) into out/keyframes
        # Save metadata into out/metadata
        
        print(f"Extracting keyframes from video: {video_path}")                    

        # Extract video name
        video_name = "_".join(os.path.splitext(os.path.basename(video_path))[:1])

        # ffmpeg command to detect shots
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"select='eq(n\,0)+gt(scene,{self.scene_threshold})',showinfo",
            '-vsync', 'vfr',
            '-q:v', '2', 
            '-frame_pts', 'true',
            f'{self.keyframe_output_path}/{video_name}_%03d.png'
        ]
        
        # Save metadata
        metadata_file = os.path.join(self.metadata_output_path, f'{video_name}_metadata.txt')

        # Run ffmpeg command
        with open(metadata_file, 'w') as f:
            subprocess.run(command, stderr=f)

                   
    def extractShotData(self, video_path):
        # Read metadata file and write to human-readable csv
        print(f"Processing metadata from video: {video_path}")                    

        video_name = video_path.stem
        metadata_file = os.path.join(self.metadata_output_path, f'{video_name}_metadata.txt')

        # Sort based on keyframe's frame index number
        keyframe_images = sorted([f for f in self.keyframe_output_path.iterdir() if f.stem.startswith(video_name)],
                                 key=lambda x: self.getFrameIndex(x.name))
        

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
                frame_index = self.getFrameIndex(keyframe_file.name)
                pts_time = pts_time_arr[i]
                hours = int(pts_time // 3600)
                minutes = int((pts_time % 3600) // 60)
                seconds = pts_time % 60
                timestamp = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
                clip_index = self.current_clip_index

                self.current_clip_index += 1

                csv_writer.writerow([video_name, frame_index, timestamp, pts_time, clip_index])

    def getFrameIndex(self, videoName: str):
        return int(videoName.split("_")[-1][:-4])

if (__name__ == "__main__"):
    # Usage example
    detector = KeyframeExtractor(scene_threshold=0.3)
    detector.processVideos()
