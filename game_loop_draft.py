# Authors: Anthony Silva and Brandon Ramirez
# Date: 4/13/24
# File: game loop draft
# Description: file for testing regular game loop operation

# imports
import cv2
import time
from ultralytics import YOLO

import data_helpers as dh
import error_detection as ed
import pose_keypoints as pk

# helper functions 
def init_camera():
    # streaming window
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3)) # get window width
    frame_height = int(cap.get(4)) # get window height

    # set fps
    cap.set(cv2.CAP_PROP_FPS, dh.FRAME_RATE)

    # normalization window
    norm_box_length = 250
    norm_box = [
        (frame_width - norm_box_length) // 2, # left bound
        (frame_height - norm_box_length) // 2, # bottom bound 
        (frame_width + norm_box_length) // 2, # right bound 
        (frame_height + norm_box_length) // 2, # top bound
    ]
    stuff = {
        "cap" : cap,
        "norm_box" : norm_box,
        "frame_dimensions" : (frame_width, frame_height),
        "norm_box_dimensions" : (norm_box_length, norm_box_length),
    }
    return stuff

def init_body():
    right_arm = [6, 10]
    left_arm = [5, 9]
    left_leg = [12, 14]
    right_leg = [11, 13]
    body = [right_arm, left_arm, right_leg, left_leg]
    return body

def run_model(frame, model, args=None):

    # run model
    if args:
        results = model(frame, show=args.show, verbose=False)
    else:
        results = model(frame, verbose=False)
    
    # extract good stuff
    keypoints = results[0].keypoints.xy[0]
    boxes = results[0].boxes
    try:
        box = boxes.xyxy[0]
    except:
        box = [0,0,0,0]
        
    stuff = {
        "keypoints" : keypoints,
        "box" : box,
    }
    return stuff 

# init source csv, also get source video
csv_fp = "./data/test_csvs/floss.csv"
keys_df = dh.load_csv_from_file(csv_fp)
video_fp = "./data/test_videos/floss.mp4"
video_frames = dh.load_video_from_file(video_fp) # can either load
video_frames_right_bound = len(video_frames) - 1 # assumes keypoints df and video_frames are aligned (as they are from the same source material) keypoint csv capture is at 25 fps right now and video frame output is at 25 fps

model = YOLO("yolov8n-pose.pt")

camera_stuff = init_camera()
cap = camera_stuff["cap"]
window_caption = "Dance Planet"

body = init_body()

# frame counter for aligning camera output with with source video, works bc both camera input and source vid input should be aligned fps
frame_counter = 0

# countdown init
start_time = time.time()
countdown = 3

# display countdown
while cap.isOpened():
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
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(current_count), (50, 50), font, 2, (255, 0, 0), 3, cv2.LINE_AA)

    # Display the resulting frame
    caption = "Get in position!"
    cv2.putText(frame, caption, (50, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame
    cv2.imshow(window_caption, frame)

    # Break the loop with 'Q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # get keypoints and bounding box from model
    model_stuff = run_model(frame, model)
    # get normalized body list by using camera frame size, model output, and standard body limb setup
    norm_body = pk.body_normalize(camera_stuff, model_stuff, body)

    # error calculation
    # setup temporal range
    temporal_size = 5 # establishes a range of (n - temporal_size, n + temporal_size) working on frame n to calculate error on
    temporal_left_bound = frame_counter - temporal_size if frame_counter - temporal_size >= 0 else 0
    temporal_right_bound = frame_counter + temporal_size if frame_counter + temporal_size <= video_frames_right_bound else video_frames_right_bound
    temporal_frame_range = [temporal_left_bound, temporal_right_bound]
    # get source keypoints for comparison
    source_bodies_raw = dh.get_keypoints_from_df_range(keys_df, temporal_frame_range)
    # convert to usable keypoints
    source_bodies_usable = [dh.usable_keypoints(keys) for keys in source_bodies_raw]
    # get error
    error = ed.min_temporal_pose_error(source_bodies_usable, norm_body)

    # display on screen
    caption = f"Error: {error}"
    source_frame = video_frames[frame_counter]
    cv2.putText(source_frame, caption, (50, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame
    cv2.imshow(window_caption, source_frame)

    #increment
    frame_counter += 1

    # end if frame_counter reaches end
    if frame_counter == video_frames_right_bound + 1:
        break

    # break loop if q
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()