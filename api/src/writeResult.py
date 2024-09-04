import numpy as np
import pandas as pd
import csv
import os
from pathlib import Path
from datetime import datetime

class WriteResult:
    submit_dir = './out/submit'
   
    def __init__(self):
        self.submit_path = Path(self.submit_dir)  

        if not os.path.exists(self.submit_path):
            os.makedirs(self.submit_path, exist_ok=True)

    def write_to_csv(self, result_df: pd.DataFrame):
        # Write the results to a csv file

        # extract the video name and frame index
        answer_df = result_df[['video_name', 'frame_index']]

        # Define the output file path

        time_of_query = datetime.now()
        hour = time_of_query.hour
        minute = time_of_query.minute
        second = time_of_query.second
        day = time_of_query.day
        month = time_of_query.month
        year = time_of_query.year

        output_file = self.submit_path / f'{hour:02d}h{minute:02d}m{second:02d}_{day:02d}_{month:02d}_{year:04d}.csv'
        
        # Write the results to a csv file
        answer_df.to_csv(output_file, index=False, header=False)

        print(f"Results written to {output_file}")



        


