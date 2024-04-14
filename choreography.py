# Authors: Anthony Silva, Brandon Ramirez
# Date: 4/13/24
# File : Choreograpy
# description : holds song information as a choreography class

import data_helpers as dh

class Choreography:

    root_csv_path = "./data/full_csvs/"
    root_video_path = "./data/test_videos/"
    root_icon_path = "./data/icons/"

    def __init__(self, name : str, threshold : float, above_ratio : float, below_ratio : float, temporal_size : int, sma_window : int, min_error : float, max_error : float):
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

        # add audio?

        # load paths
        self.df = dh.load_csv_from_file(self.csv_path)
        self.video_frames = dh.load_video_from_file(self.mp4_path)
        self.icon = dh.load_image_from_file(self.icon_path)
    
    @classmethod
    def load_many_from_csv(fp : str):
        chors = []
        chor_df = dh.load_csv_from_file(fp)
        for row in chor_df.itertuples(index=False):
            chor = Choreography(row.name, row.threshold, row.above_ration, row.below_ratio, row.temporal_size, row.sma_winow, row.min_error, row.max_error)
            chors.append(chor)
        return chors

    @classmethod
    def get_chor_from_chors(name : str, chors : list):
        for chor in chors:
            if chor.name == name:
                return chor
        return "chor not found!"