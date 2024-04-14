
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

# helper functions 
def init_camera():
    """
    capture is either 0 or fp to video for comparison
    """
    # streaming window
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3)) # get window width
    frame_height = int(cap.get(4)) # get window height

    # set fps
    cap.set(cv2.CAP_PROP_FPS, dh.FRAME_RATE)

    # normalization window
    norm_box_width = 200
    norm_box_height = 300
    mid_width = frame_width // 2
    mid_height = frame_height // 2
    gap = 15

    norm_box_0 = [
        (frame_width - norm_box_width) // 2, # left bound
        (frame_height - norm_box_height) // 2, # bottom bound , or top bound?
        (frame_width + norm_box_width) // 2, # right bound 
        (frame_height + norm_box_height) // 2, # top bound, or bototm boudn?
    ]
    start_x = mid_width - norm_box_width
    bottom_y = frame_height - norm_box_height
    norm_box_1 = [
        start_x - gap, # left
        bottom_y - gap, # bottom
        start_x - gap + norm_box_width, # right
        frame_height - gap # top
    ]
    norm_box_2 = [
        start_x + norm_box_width + gap, # left
        bottom_y - gap, # bottom
        start_x + gap + norm_box_width * 2,  #ight
        frame_height - gap # top
    ]
    stuff = {
        "cap" : cap,
        "norm_box_0" : norm_box_0,
        "norm_box_1" : norm_box_1,
        "norm_box_2" : norm_box_2,
        "frame_dimensions" : (frame_width, frame_height),
        "norm_box_dimensions" : (norm_box_width, norm_box_height),
    }
    return stuff

def init_camera_v2(controller):
    """
    capture is either 0 or fp to video for comparison
    """
    # streaming window
    cap = controller.cap
    frame_width = int(cap.get(3)) # get window width
    frame_height = int(cap.get(4)) # get window height

    # set fps
    cap.set(cv2.CAP_PROP_FPS, dh.FRAME_RATE)

    # normalization window
    norm_box_width = 200
    norm_box_height = 300
    mid_width = frame_width // 2
    mid_height = frame_height // 2
    gap = 15

    norm_box_0 = [
        (frame_width - norm_box_width) // 2, # left bound
        (frame_height - norm_box_height) // 2, # bottom bound , or top bound?
        (frame_width + norm_box_width) // 2, # right bound 
        (frame_height + norm_box_height) // 2, # top bound, or bototm boudn?
    ]
    start_x = mid_width - norm_box_width
    bottom_y = frame_height - norm_box_height
    norm_box_1 = [
        start_x - gap, # left
        bottom_y - gap, # bottom
        start_x - gap + norm_box_width, # right
        frame_height - gap # top
    ]
    norm_box_2 = [
        start_x + norm_box_width + gap, # left
        bottom_y - gap, # bottom
        start_x + gap + norm_box_width * 2,  #ight
        frame_height - gap # top
    ]
    stuff = {
        "cap" : cap,
        "norm_box_0" : norm_box_0,
        "norm_box_1" : norm_box_1,
        "norm_box_2" : norm_box_2,
        "frame_dimensions" : (frame_width, frame_height),
        "norm_box_dimensions" : (norm_box_width, norm_box_height),
    }
    return stuff

def init_body():
    right_arm = [6, 10]
    left_arm = [5, 9]
    left_leg = [12, 14]
    right_leg = [11, 13]
    body = [right_arm, left_arm, right_leg, left_leg]
    return body

def init_body_v2():
    right_upper_arm = [5, 7]
    right_forearm = [7, 9]
    left_upper_arm = [6, 8]
    left_forearm = [8, 10]
    right_quad = [11, 13]
    right_calf = [13, 15]
    left_quad = [12, 14]
    left_calf = [14, 16]
    body = [right_upper_arm, right_forearm, left_upper_arm, left_forearm, right_quad, right_calf, left_quad, left_calf]
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

def create_analytics(time, data):
    # create an index list from 0 to length of differences list
    fig, ax = plt.subplots()

    # plot the data 
    ax.plot(time, data, marker='o', linestyle='-', color='b')

    # add title and labels 
    ax.set_title('Differences Over Time')
    ax.set_xlabel('Time Index')
    ax.set_ylabel('Difference')

    # save plot to bytesio buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # load buffer into numpy and convert to opencv image
    image = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    plt.close(fig)

    # return image
    return image

def add_limbs_to_frame(norm_body : list, norm_box : list, frame : np.array):
    # color
    line_color = (255, 0, 0)
    line_thickness = 1
    circle_color = (0, 255, 0)
    circle_radius = 3
    circle_thickness = 4
    rectangle_color = (102, 51, 153)
    rectangle_thickness = 4

     # limb is not visible if points are [[0, 0], [0, 0]]
    invisible_limb = [[0, 0], [0, 0]]
    visibility = [limb != invisible_limb for limb in norm_body]
    for i, limb in enumerate(norm_body):
        if visibility[i]:
            start = [a + b for a,b in zip(limb[0], [norm_box[0], norm_box[1]])]
            end = [a + b for a,b in zip(limb[1], [norm_box[0], norm_box[1]])]
            cv2.line(frame, start, end, line_color, line_thickness)
            cv2.circle(frame, start, radius=circle_radius, color=circle_color, thickness=circle_thickness)
            cv2.circle(frame, end, radius=circle_radius, color=circle_color, thickness=circle_thickness)
    
    # show norm square
    cv2.rectangle(frame, (norm_box[0], norm_box[1]), (norm_box[2], norm_box[3]), color=rectangle_color, thickness=rectangle_thickness)
    
    return frame

def visibility_score(player_body : list) -> int:
    visibility_count = 0
    for limb in player_body:
        if limb != [[0, 0], [0, 0]]:
            visibility_count += 1
    return visibility_count

def body_printout(body):
    print(f"right arm: {body[0]} || x_len : {body[0][1][0] - body[0][0][0]} || y_len: {body[0][1][1] - body[0][0][1]}")
    print(f"left arm: {body[1]} || x_len : {body[1][1][0] - body[1][0][0]} || y_len: {body[1][1][1] - body[1][0][1]}")
    print(f"right leg: {body[2]} || x_len : {body[2][1][0] - body[2][0][0]} || y_len: {body[2][1][1] - body[2][0][1]}")
    print(f"left leg: {body[3]} || x_len : {body[3][1][0] - body[3][0][0]} || y_len: {body[3][1][1] - body[3][0][1]}")
