# Authors: Anthony Silva and Brandon Ramirez
# Date : 4/13/24
# File : battle mode
# description : script for taking brunt work of battle mode

# imports
import cv2
import time
from ultralytics import YOLO
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

import data_helpers as dh
import error_detection as ed
import pose_keypoints as pk
import dance_comparison_helpers as dch
import practice_mode_helpers as pmh
from choreography import Choreography

def battle_mode(dances : list, test_dance, flags):
    """
    takes the brunt work of the battle mode handling
    args:
        - dances : list of choreography objects made from the selection of battle mode
        - test_dance : either 0 for webcam or string for filepath to video to use
        - flags : dictionary of flags for running the game:
            flags = {
                "countdown" : (bool) # is countdown enabled?
            }
    returns:
    """

    # general init
    body = dch.init_body_v2()
    
    model = YOLO('yolov8n-pose.pt')

    camera_stuff = dch.init_camera(test_dance)
    cap = camera_stuff["cap"]
    window_caption = "Dance Planet"
    font = cv2.FONT_HERSHEY_SIMPLEX

    # frame counter for aligning camera output with source video, all should be 25 fps
    frame_counter = 0

    # countdown if enabled
    countdown = 5
    cd = flags["countdown"]
    countdown_messages = [
        "Get ready Player 1!",
        "Get ready Player 2!"
    ]
    current_msg = 0

    if cd:
        pmh.countdown(cap, countdown, countdown_messages[current_msg])
        current_msg = 0 if current_msg else 1 # swap countdown message based on what it was last


