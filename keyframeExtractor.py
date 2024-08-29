from pathlib import Path
import subprocess

class keyframeExtractor:
    def extract_keyframes(self, video_path, output_folder):
        output_folder.mkdir(parents=True, exist_ok=True)
        video_name = video_path.stem

        ffmpeg_command = [
            'ffmpeg',
            '-skip_frame', 'nokey', 
            '-i', str(video_path), 
            '-vsync', 'vfr',
            '-q:v', '2', 
            '-frame_pts', 'true',
            str(output_folder / f'{video_name}_keyframe_%04d.jpg')
        ]

        subprocess.run(ffmpeg_command)

    def process_videos(self, data_dir, output_dir):
        data_dir = Path(data_dir)
        output_path = Path(output_dir)
        
        folder_paths = sorted(data_dir.iterdir(), key=lambda x: x.name)
        
        for folder_path in folder_paths:
            if folder_path.is_dir():  
                video_paths = sorted(folder_path.glob('*.mp4')) 

                for video_path in video_paths:
                    output_folder = output_path
                    self.extract_keyframes(video_path, output_folder)


data = './Video'
output = './Keyframes'
extract = keyframeExtractor()
extract.process_videos(data, output)
