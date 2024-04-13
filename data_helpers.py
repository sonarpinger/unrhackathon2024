# Authors: Anthony Silva and Brandon Ramirez
# Date: 4/12/24
# File: Data helpers
# Description: module for helping extract static data, extract frames, keypoints from videos/frames

import cv2
import numpy as np
import pandas as pd

FRAME_RATE = 25

def load_image_from_file(image_fp : str) -> np.array:
    image = cv2.imread(image_fp)
    if image is not None:
        return image
    else:
        raise FileNotFoundError(f"No image found at {image_fp}")

def load_video_from_file(video_fp : str) -> list:
    """
    takes in a filepath of a video and extracts the video frame by frame at the desired FRAME_RATE into a list of frames and returns the list of frames
    """
    cap = cv2.VideoCapture(video_fp)
    if not cap.isOpened():
        raise FileNotFoundError(f"No video found at {video_fp}")
    
    # Get the original video framerate
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    skip_frames = int(original_fps / FRAME_RATE)
    
    frames = []
    frame_counter = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if frame_counter % skip_frames == 0:
                frames.append(frame)
            frame_counter += 1
        else:
            break
    
    cap.release()
    return frames

def get_frame_from_video(video : list, index : int) -> np.array:
    """
    gets a specific index from the list of frames in the video
    """
    if index < 0 or index >= len(video):
        raise IndexError("Frame index out of range")
    return video[index]

def get_frames_from_video(video : list, frame_range : list) -> list:
    """
    gets a range of frames from the list of frames in the video
    """
    if frame_range[0] < 0 or frame_range[1] > len(video):
        raise IndexError("Frame range out of bounds")
    return video[frame_range[0]:frame_range[1]]

def load_csv_from_file(csv_file_path : str) -> pd.DataFrame:
    """
    Load a csv of YOLO keypoint outputs (from output_csv.py) into a pd.DataFrame
    """
    try:
        keypoints_df = pd.read_csv(csv_file_path)
        return keypoints_df
    except FileNotFoundError:
        raise FileNotFoundError(f"No CSV file found at {csv_file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the CSV file: {str(e)}")

def get_keypoints_from_df(keypoint_df : pd.DataFrame, index : int) -> list:
    """
    Get a specified keypoint row from the dataframe 
    """
    series_row = keypoint_df.iloc[index]
    keypoints = series_row.tolist()
    return keypoints

def get_keypoints_from_df_range(keypoints_df : pd.DataFrame, range : list) -> list:
    """
    Get a continuous list of keypoint rows from the dataframe
    """
    sub_df = keypoints_df.iloc[range[0]:range[1]] # extract the rows
    keypoints_list = sub_df.values.tolist() # convert to list of lists
    return keypoints_list


def usable_keypoints(keypoints_list : list) -> list:
    """
    Move row keypoints from their dataframe format to something usable from the error function
    Format:
    right_arm_start_x,right_arm_start_y,right_arm_end_x,right_arm_end_y,
    left_arm_start_x,left_arm_start_y,left_arm_end_x,left_arm_end_y,
    right_leg_start_x,right_leg_start_y,right_leg_end_x,right_leg_end_y,
    left_leg_start_x,left_leg_start_y,left_leg_end_x,left_leg_end_y
    """
    # extract starts/ends of limb vectors
    right_arm_start = [keypoints_list[0], keypoints_list[1]]
    right_arm_end = [keypoints_list[2], keypoints_list[3]]
    left_arm_start = [keypoints_list[4], keypoints_list[5]]
    left_arm_end = [keypoints_list[6], keypoints_list[7]]
    right_leg_start = [keypoints_list[8], keypoints_list[9]]
    right_leg_end = [keypoints_list[10], keypoints_list[11]]
    left_leg_start = [keypoints_list[12], keypoints_list[13]]
    left_leg_end = [keypoints_list[14], keypoints_list[15]]
    # put into body
    body = [
        [right_arm_start, right_arm_end],
        [left_arm_start, left_arm_end],
        [right_leg_start, right_leg_end],
        [left_leg_start, left_leg_end]
    ]
    return body