# Authors: Anthony Silva, Brandon Ramirez
# Date: 4/13/24
# File: draft2
# description: for testing modular dance comparison loop

import dance_comparison as dc
import cv2
import numpy as np

# same video (anthonyfloss) averages ~230
# anthonyfloss test on orangejustice video averages ~300-350
# flossanthony test on source floss-new averages 200
# two orangejustices: 350
# testing oj on get griddy source: 400

# testing lots on get griddy
# oj : 400
# griddy : 241

source_dance = "flossanthony"
# test_dance = "./data/test_videos/flossanthony.mp4"
test_dance = 0
error_parameters = {
    "threshold" : 0,
    "above_ratio" : 1.0,
    "below_ratio" : 0.5,
    "temporal_size" : 25,
}
flags = {
    "analytics" : False,
    "limb_view" : True,
    "data_printout" : False,
    "countdown" : False,
}

def display_chart(image):
    if image is not None:
        # Display the image
        cv2.imshow('Image', image)

        # Wait for any key to be pressed before closing
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Image not found")

def display_frames(frames):
    caption = "frameplayback"
    for img in frames:
        if img is None:
            print("Bad Image")
            continue
        
        cv2.imshow('Image Sequence', img)  # Display the image
        k = cv2.waitKey(100)  # Wait for x milliseconds
        
        if k == 27:  # If 'ESC' is pressed, break the loop
            break

output = dc.dance_comparison(source_dance, test_dance, error_parameters, flags)
chart = output["chart"] # if output["chart"] else None 
frames = output["frames"] # if output["frames"] else None
errors = output["errors"]

print(f"Avg error: {np.average(errors)}")