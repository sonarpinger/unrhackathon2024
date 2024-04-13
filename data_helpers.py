# Authors: Anthony Silva and Brandon Ramirez
# Date: 4/12/24
# File: Data helpers
# Description: module for helping extract static data, extract frames, keypoints from videos/frames

import cv2
import numpy as np

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

def get_frames_from_video(video : list, frame_range : range) -> list:
    """
    gets a range of frames from the list of frames in the video
    """
    if frame_range.start < 0 or frame_range.stop > len(video):
        raise IndexError("Frame range out of bounds")
    return [video[i] for i in frame_range]