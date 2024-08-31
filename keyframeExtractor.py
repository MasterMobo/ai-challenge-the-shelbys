import subprocess
import os
import re
import csv
from pathlib import Path

class KeyframeExtractor:
    def __init__(self, scene_threshold=0.3):
        self.scene_threshold = scene_threshold

    def detect_shots(self, video_path, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"select='gt(scene,{self.scene_threshold})',showinfo",
            '-vsync', 'vfr',
            '-q:v', '2', 
            '-frame_pts', 'true',
            f'{output_dir}/{video_name}_%03d.png'
        ]

        metadata_file = os.path.join(output_dir, f'{video_name}_metadata.txt')

        with open(metadata_file, 'w') as f:
            subprocess.run(command, stderr=f)

        print(f"Shot detection completed. Keyframes saved in {output_dir}. Metadata saved as {metadata_file}.")

    def extract_shot_data(self, video_path, output_dir):
        video_name = os.path.basename(video_path)
        video_name = os.path.splitext(video_name)[0]        
        metadata_file = os.path.join(output_dir, f'{video_name}_metadata.txt')
        output_file = os.path.join(output_dir, f'{video_name}_metadata_processed.csv')


        keyframe_images = sorted(
            [f for f in os.listdir(output_dir) if f.endswith('.png')],
            key=lambda x: int(re.search(r'_(\d+)\.png$', x).group(1)) 
        )

        with open(metadata_file, 'r') as f, open(output_file, 'w', newline='') as out_f:
            csv_writer = csv.writer(out_f)
            csv_writer.writerow(['file_name', 'video_name', 'frame_index', 'timestamp'])

            frame_timestamps = {}
            pts_time_arr = []

            for keyframe_file in keyframe_images:
                frame_index = int(re.search(r'_(\d+)\.png$', keyframe_file).group(1))
                frame_timestamps[frame_index] = 0

            for line in f:
                if 'pts_time' in line:
                    pts_time = float(line.split('pts_time:')[1].split(' ')[0])
                    pts_time_arr.append(pts_time)

            i = 0        
            for keyframe_file in keyframe_images:
                frame_index = int(re.search(r'_(\d+)\.png$', keyframe_file).group(1))
                if i < len(pts_time_arr):
                    frame_timestamps[frame_index] = pts_time_arr[i]
                    i += 1   

            for keyframe_file in keyframe_images:
                frame_index = int(re.search(r'_(\d+)\.png$', keyframe_file).group(1))
                if frame_index in frame_timestamps:
                    pts_time = frame_timestamps[frame_index]
                    hours = int(pts_time // 3600)
                    minutes = int((pts_time % 3600) // 60)
                    seconds = pts_time % 60
                    timestamp = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

                    csv_writer.writerow([keyframe_file, video_name, frame_index, timestamp])
                else:
                    csv_writer.writerow([keyframe_file, video_name, 'N/A', 'N/A'])

    def process_videos(self, data_dir, output_dir):
        data_dir = Path(data_dir)
        output_path = Path(output_dir)
        
        folder_paths = sorted(data_dir.iterdir(), key=lambda x: x.name)
        
        for folder_path in folder_paths:
            if folder_path.is_dir():  
                video_paths = sorted(folder_path.glob('*.mp4')) 

                for video_path in video_paths:
                    output_folder = output_path / folder_path.name / video_path.stem
                    self.detect_shots(video_path, output_folder)
                    self.extract_shot_data(video_path, output_folder)

# Usage example
data_dir = './Video'
output_dir = './data/keyframes'

detector = KeyframeExtractor(scene_threshold=0.3)

detector.process_videos(data_dir, output_dir)
