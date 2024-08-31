import subprocess
import os
import csv
from pathlib import Path

class KeyframeExtractor:
    data_dir = './data/videos'
    output_dir = './out/keyframes'

    def __init__(self, scene_threshold=0.3):
        self.scene_threshold = scene_threshold

    def processVideos(self):
        # Iterate through each video to extract keyframes and metadata

        # Create paths from directory
        data_path = Path(self.data_dir)
        output_path = Path(self.output_dir)
        
        folder_paths = data_path.iterdir()
        
        # Process each folder
        for folder_path in folder_paths:
            if folder_path.is_dir():
                video_paths = folder_path.iterdir()

                for video_path in video_paths:
                    video_output_path = output_path / folder_path.name / video_path.stem
                    
                    self.detectShots(video_path, video_output_path)
                    self.extractShotData(video_path, video_output_path)

    def detectShots(self, video_path, video_output_path):
        # Detect shots in a video and save keyframes and metadata
        # Save keyframes (as PNG's) and metadata into data/keyframes/{folder_name}/{video_name}/

        os.makedirs(video_output_path, exist_ok=True)

        # Extract video name
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        #ffmpeg command to detect shots
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"select='gt(scene,{self.scene_threshold})',showinfo",
            '-vsync', 'vfr',
            '-q:v', '2', 
            '-frame_pts', 'true',
            f'{video_output_path}/{video_name}_%03d.png'
        ]
        
        # Save metadata
        metadata_file = os.path.join(video_output_path, f'{video_name}_metadata.txt')

        # Run ffmpeg command
        with open(metadata_file, 'w') as f:
            subprocess.run(command, stderr=f)

        print(f"Shot detection completed. Keyframes saved in {video_output_path}. Metadata saved as {metadata_file}.")
                   
    def extractShotData(self, video_path, output_dir):
        # Read metadata file and write to human-readable csv

        video_name = os.path.splitext(os.path.basename(video_path))[0]        
        metadata_file = os.path.join(output_dir, f'{video_name}_metadata.txt')
        output_file = os.path.join(output_dir, f'{video_name}_metadata_processed.csv')

        # Sort based on keyframe's frame index number
        keyframe_images = sorted(
            [f for f in os.listdir(output_dir) if f.endswith('.png')],
            key=lambda videoName: self.getFrameIndex(videoName) 
        )
        
        # Read from metadata and write to .csv file
        with open(metadata_file, 'r') as f, open(output_file, 'w', newline='') as out_f:
            csv_writer = csv.writer(out_f)

            #  Headers
            csv_writer.writerow(['file_name', 'video_name', 'frame_index', 'timestamp', 'pts_time'])

            pts_time_arr = []

            # Find and append pts_time to pts_time_arr
            for line in f:
                if 'pts_time' in line:
                    pts_time = float(line.split('pts_time:')[1].split(' ')[0])
                    pts_time_arr.append(pts_time)

            # Save to csv file
            for i, keyframe_file in enumerate(keyframe_images):
                frame_index = self.getFrameIndex(keyframe_file)
                pts_time = pts_time_arr[i]
                hours = int(pts_time // 3600)
                minutes = int((pts_time % 3600) // 60)
                seconds = pts_time % 60
                timestamp = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

                csv_writer.writerow([keyframe_file, video_name, frame_index, timestamp, pts_time])

    def getFrameIndex(self, videoName: str):
        return int(videoName.split("_")[-1][:-4])

if (__name__ == "__main__"):
    # Usage example
    detector = KeyframeExtractor(scene_threshold=0.3)
    detector.processVideos()
