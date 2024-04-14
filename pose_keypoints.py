# Authors: Anthony Silva and Brandon Ramirez
# Date: 4/12/24
# File: Pose Keypoints
# Description: module for extracting pose from keypoints and normalizing them

def horizontal_body_flip(frame_stuff : dict, body : list) -> list:
    """
    performs a horizontal flip transformation on the body based on frame structure
    args:
        - frame_stuff {
                "norm_box_dimensions" : (x, y)
                ...
            }
        - list of limb vectors [ [[x1, y1], [x2, y2]] , ...] where xi, yi lie within norm box dimensions
    returns:
        - flipped_body which is a horizontal flip of the body list based on the norm box dimensions 
    """
    # Extract the width of the normalization box
    norm_box_width, _ = frame_stuff["norm_box_dimensions"]

    # Calculate the horizontal midpoint of the normalization box
    horizontal_midpoint = norm_box_width // 2

    # Initialize the list for the flipped body
    flipped_body = []

    # Loop over each limb in the body
    for limb in body:
        flipped_limb = []
        for point in limb:
            x, y = point
            # Flip the y-coordinate
            flipped_x = 2 * horizontal_midpoint - x
            # Append the flipped point to the flipped limb
            flipped_limb.append([flipped_x, y])
        # Append the flipped limb to the flipped body
        flipped_body.append(flipped_limb)

    return flipped_body


def body_normalize(frame_stuff : dict, model_stuff : dict, body : list) -> list:
    """
    Takes keypoints and creates normalized limbs based on size of person and size of input window
    Args:
        - frame_stuff {
            "norm_box_dimensions" : (x, y)
            ...
        }
        - model_stuff {
            "keypoints" : keypoints form person from YOLO
            "box" : person obj detect box fro YOLO
            ...
        }
        - body : list of keypoints to limb mappings
    returns norm_body which is a list of limb vectors like this: [ [[x1, y1], [x2, y2]], ...]
    """

    # get model results 
    keypoints = model_stuff['keypoints']
    box = model_stuff["box"]

    # get camera stuff
    norm_width = frame_stuff['norm_box_dimensions'][0]
    norm_height = frame_stuff['norm_box_dimensions'][1]

    box_start = [int(box[0]), int(box[1])]

    # get norm vectors
    norm_body = []
    # only work on visible keypoints
    visible = [i for i in range(keypoints.shape[0]) if keypoints[i][0] != 0 and keypoints[i][1] != 0]
    for limb in body:
        if limb[0] in visible and limb[1] in visible:
            start = keypoints[limb[0]]
            end = keypoints[limb[1]]
            norm_start = [ # start of the normalized limb vector
                int( # cast to int for graphing
                    (start[0] - box_start[0]) * norm_width / (box[2] - box[0]) # offset to horizontal left, multiply by normalization width, divide by width of person box
                ),
                int(
                    (start[1] - box_start[1]) * norm_height / (box[3] - box[1]) # offset to vertical bottom, multiply by normalization height, divide by height of person box 
                )
            ]
            norm_end = [ # end of the normalized limb vector
                int(
                    (end[0] - box_start[0]) * norm_width / (box[2] - box[0]) # offset to horizontal left, multiply by normalized width, divide by width of person box
                ),
                int(
                    (end[1] - box_start[1]) * norm_height / (box[3] - box[1]) # offset to vertical bottom, multiple by normalized height, divide by height of person box 
                )
            ]
            norm_limb = [norm_start, norm_end] # got normed limb!
        else:
            norm_limb = [[0, 0], [0, 0]] # standard value for limb that doesnt exist (isnt visible)
        norm_body.append(norm_limb)
    
    return norm_body