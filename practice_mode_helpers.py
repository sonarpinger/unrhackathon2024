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
from choreography import Choreography

def countdown(cap, countdown_time, font):
    """
    performs a countdown for practice mode
    """

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # calculate the time elapsed
        elapsed_time = time.time() - start_time
        
        # Update the countdown
        current_count = countdown_time - int(elapsed_time)
        if current_count < 0:
            # end countdown if reaches end time (less than 0)
            break
        
        # Put the countdown text on the frame
        cv2.putText(frame, str(current_count), (50, 50), font, 2, (255, 0, 0), 3, cv2.LINE_AA)

        # Display the resulting frame
        caption = "Get in position!"
        cv2.putText(frame, caption, (50, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame
        cv2.imshow('practice', frame)

        # Break the loop with 'Q' key
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break