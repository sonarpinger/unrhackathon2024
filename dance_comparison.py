# Authors: Anthony Silva and Brandon Ramirez
# Date: 4/13/24
# File: Dance Comparison
# Description: modularizes running a dance to webcam or other dance comparison

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

def dance_comparison(source_dance : str, test_dance, error_parameters, flags) -> dict:
    """
    Args:
        - 
        - test_dance: either 0 (for webcam) or string of filepath to test dance
    """
    
    threshold = error_parameters["threshold"]
    above_ratio = error_parameters["above_ratio"]
    below_ratio = error_parameters["below_ratio"]
    temporal_size = error_parameters["temporal_size"]
    sma_window = error_parameters["sma_window"]
    song_min_error = error_parameters["min_error"]
    song_max_error = error_parameters["max_error"]
    score_timing = error_parameters["score_timing"]

    test_string = type(test_dance) == str

    csv_fp = f"./data/full_csvs/{source_dance}.csv"
    keys_df = dh.load_csv_from_file(csv_fp)
    video_fp = f"./data/test_videos/{source_dance}.mp4"
    video_frames = dh.load_video_from_file(video_fp)
    video_frames_right_bound = len(video_frames) - 1 # assumes keypoints df and video_frames are aligned (as they are from the same source material) keypoint csv capture is at 25 fps right now and video frame output is at 25 fps

    model = YOLO("yolov8n-pose.pt")

    camera_stuff = dch.init_camera(test_dance)
    cap = camera_stuff["cap"]
    window_caption = "Dance Planet"
    font = cv2.FONT_HERSHEY_SIMPLEX

    body = dch.init_body_v2()

    # frame counter for aligning camera output with with source video, works bc both camera input and source vid input should be aligned fps
    frame_counter = 0

    # countdown init
    start_time = time.time()
    countdown = 3
    cd = flags["countdown"] # enable countdown

    # display countdown
    while cd and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # calculate the time elapsed
        elapsed_time = time.time() - start_time
        
        # Update the countdown
        current_count = countdown - int(elapsed_time)
        if current_count < 0:
            # end countdown if reaches end time (less than 0)
            break
        
        # Put the countdown text on the frame
        cv2.putText(frame, str(current_count), (50, 50), font, 2, (255, 0, 0), 3, cv2.LINE_AA)

        # Display the resulting frame
        caption = "Get in position!"
        cv2.putText(frame, caption, (50, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame
        cv2.imshow(window_caption, frame)

        # Break the loop with 'Q' key
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    
    analytics = flags["analytics"]
    error_over_time = []
    frames = []
    chart = None

    limb_view = flags["limb_view"]

    data_printout = flags['data_printout']

    # for getting score
    last_score_time = time.time()
    total_score = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # get keypoints and bounding box from model
        model_stuff = dch.run_model(frame, model)
        # get normalized body list by using camera frame size, model output, and standard body limb setup
        norm_body = pk.body_normalize(camera_stuff, model_stuff, body)
        # add horizontal flip of keypoints if on webcam
        if not test_string:
            norm_body = pk.horizontal_body_flip(camera_stuff, norm_body)

        temporal_left_bound = frame_counter - temporal_size if frame_counter - temporal_size >= 0 else 0
        temporal_right_bound = frame_counter + temporal_size if frame_counter + temporal_size <= video_frames_right_bound else video_frames_right_bound
        temporal_frame_range = [temporal_left_bound, temporal_right_bound]
        current_source_body_index = (temporal_right_bound - temporal_left_bound) // 2
        # get source keypoints for comparison
        source_bodies_raw = dh.get_keypoints_from_df_range(keys_df, temporal_frame_range)
        # convert to usable keypoints
        source_bodies_usable = [dh.usable_keypoints_v2(keys) for keys in source_bodies_raw]
        # get error
        error = ed.min_temporal_pose_error(source_bodies_usable, norm_body, threshold, above_ratio, below_ratio)
        temp = error_over_time + [error]
        error_adjusted = ed.simple_moving_average(temp, sma_window)
        error_over_time.append(error_adjusted)

        # check score
        current_time = time.time()
        if current_time - last_score_time >= score_timing:  # Check if one second has passed
            score = ed.error_to_score(song_min_error, song_max_error, error_adjusted)  # Run the function
            total_score += score
            cv2.putText(source_frame, f"+{score} points!", (250, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            last_time_run = current_time  # Reset the last run time

        # display on screen
        caption = f"Error: {error_adjusted}"
        source_frame = video_frames[frame_counter]
        
        if analytics:
            time_indices = list(range(frame_counter + 1))
            # get chart 
            chart = dch.create_analytics(time_indices, error_over_time)

            # display
            analytics_caption = "error over time"
            cv2.imshow(analytics_caption, chart)
            plt.close()
        
        if limb_view:
            dch.add_limbs_to_frame(norm_body, camera_stuff["norm_box_1"], source_frame)
            dch.add_limbs_to_frame(source_bodies_usable[current_source_body_index], camera_stuff["norm_box_2"], source_frame)
            vis_caption = f"visibility score: {dch.visibility_score(norm_body)}"
            cv2.putText(source_frame, vis_caption, (200, 200), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame

        # data print out 
        if data_printout:
            print("norm_body : ")
            dch.body_printout(norm_body)
            print("source_body : ")
            dch.body_printout(source_bodies_usable[current_source_body_index])
            print(f"error : {error}")
            break
        
        # true display
        cv2.putText(source_frame, caption, (50, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame
        cv2.putText(source_frame, f"Score: {total_score}", (250, 250), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow(window_caption, source_frame)

        #increment
        frame_counter += 1
        frames.append(source_frame)

        # end if frame_counter reaches end
        if frame_counter == video_frames_right_bound + 1:
            break

        # break loop if q
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    # return analytics
    output = {
        "frames" : frames,
        "chart" : chart,
        "errors" : error_over_time
    }

    return output