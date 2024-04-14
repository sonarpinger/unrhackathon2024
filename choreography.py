# Authors: Anthony Silva, Brandon Ramirez
# Date: 4/13/24
# File : Choreograpy
# description : holds song information as a choreography class

import data_helpers as dh
import csv
import pandas as pd

class Choreography:

    root_csv_path = "./data/full_csvs/"
    root_video_path = "./data/test_videos/"
    root_icon_path = "./data/icons/"

    def __init__(self, name : str, threshold : float, above_ratio : float, below_ratio : float, temporal_size : int, sma_window : int, min_error : float, max_error : float, score_timing : int):
        self.name = name
        self.csv_path = self.root_csv_path + self.name + ".csv"
        self.mp4_path = self.root_video_path + self.name + ".mp4"
        self.icon_path = self.root_icon_path + self.name + ".png"
        self.threshold = threshold
        self.above_ratio = above_ratio
        self.below_ratio = below_ratio
        self.temporal_size = temporal_size
        self.sma_window = sma_window
        self.min_error = min_error
        self.max_error = max_error
        self.score_timing = score_timing

        # add audio?

        # load paths
        self.df = dh.load_csv_from_file(self.csv_path)
        self.video_frames = dh.load_video_from_file(self.mp4_path)
        self.icon = dh.load_image_from_file(self.icon_path)
    
    def to_csv(self):
        return [self.name, self.threshold, self.above_ratio, self.below_ratio, self.temporal_size, self.sma_window, self.min_error, self.max_error, self.score_timing]

    @classmethod
    def load_many_from_csv(cls, fp : str):
        chors = []
        chor_df = dh.load_csv_from_file(fp)
        for row in chor_df.itertuples(index=False):
            chor = cls(row.name, row.threshold, row.above_ratio, row.below_ratio, row.temporal_size, row.sma_window, row.min_error, row.max_error, row.score_timing)
            chors.append(chor)
        return chors

    @classmethod
    def get_chor_from_chors(cls, name : str, chors : list):
        for chor in chors:
            if chor.name == name:
                return chor
        raise Exception("chor not found!")

    @classmethod
    def save_chor_to_csv(cls, fp: str, chor):
        with open(fp, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(chor.to_csv()) 
    
    @classmethod
    def get_chor_from_csv(cls, fp: str, name : str):
        chors_df = pd.read_csv(fp)
        row = chors_df[chors_df["name"] == name].iloc[0]
        chor = cls(name = row["name"], 
                   threshold = row["threshold"], 
                   above_ratio = row["above_ratio"], 
                   below_ratio = row["below_ratio"], 
                   temporal_size = row["temporal_size"], 
                   sma_window = row["sma_window"], 
                   min_error = row["min_error"], 
                   max_error = row["max_error"], 
                   score_timing = row["score_timing"])
        return chor