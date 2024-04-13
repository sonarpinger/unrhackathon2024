# Authors: Anthony Silva and Brandon Ramirez
# Date: 4/12/24
# File: Error Detection
# Description: module for holding all functions relating to pose detection

import numpy as np

def limb_delta(limb_truth : list, limb_test : list) -> float:
    """
    Takes two limbs, each of structure [[x1, y1], [x2, y2]], and calculates the difference between them
    """
    _difference = [
        [abs(limb_truth[i][j] - limb_test[i][j]) for j in range(len(limb_truth[i]))] for i in range(len(limb_test))
    ]
    difference = sum(sum(inner_list) for inner_list in _difference) # add each difference between the keypoints
    return difference

def delta_linear_scalar(difference : float) -> float:
    """
    scale the error to be more dramatic the further away it is
    implements linear scaling
    """
    old_min, old_max = 250, 2500
    new_min, new_max = 250, 100000
    scaled_dif = new_min + (difference - old_min) * (new_max - new_min) / (old_max - old_min)
    return scaled_dif


def get_difference(limb_truth : list, limb_test : list) -> float:
    """
    performs all the calcs needed to get a difference between two limbs
    """
    simple_dif = limb_delta(limb_truth, limb_test)
    scaled_dif = delta_linear_scalar(simple_dif)
    return scaled_dif


def simple_pose_error(body_truth : list, body_test : list) -> float:
    """
    A simple error function that takes the total difference between two body lists, 
    where each entry i in both lists correspond to a specific limb vector of structure [[x1, y1], [x2, y2]]
    """
    error_sum = 0 # keep track of total error of all limbs
    for i, limb_truth in enumerate(body_truth):
        limb_test = body_test[i]
        error = get_difference(limb_truth, limb_test) # get error for that limb
        error_sum += error # add
    return error_sum # return total sum of differences as an error

def avg_temporal_pose_error(_body_truth : list, body_test : list) -> float:
    """
    Takes an input body list (pose) and compares it to multiple frame source material and outputs the average
    Args:
        - _body_truth [ [[[x1, y1], [x2, y2]], [[x1, y1], [x2, y2]], ... ], ... ] : list of source vectors to compare to
        - body_test [[[x1, y1], [x2, y2]], [[x1, y1], [x2, y2]], ...] : list of limb vectors (body pose)
    Returns:
        - error_avg (float) : average error among the whole set
    """
    error_sum = 0
    counter = 0
    for body_truth in _body_truth:
        error = simple_pose_error(body_truth, body_test)
        error_sum += error
        counter += 1
    error_avg = error_sum / counter
    return error_avg

def min_temporal_pose_error(_body_truth : list, body_test : list) -> float:
    """
    Takes in input body list (pose) and compares it to multiple frame source material and outputs the min error 
    Args:
        - _body_truth [ [[[x1, y1], [x2, y2]], [[x1, y1], [x2, y2]], ... ], ... ] : list of source vectors to compare to
        - body_test [[[x1, y1], [x2, y2]], [[x1, y1], [x2, y2]], ...] : list of limb vectors (body pose)
    Returns:
        - error_min (float) : min error among the whole set
    """
    min_error = 1000000000000000
    for body_truth in _body_truth:
        error = simple_pose_error(body_truth, body_test)
        if error < min_error:
            min_error = error
    return min_error

def max_temporal_pose_error(_body_truth : list, body_test : list) -> float:
    """
    Takes in input body list (pose) and compares it to multiple frame source material and outputs the max error
    Args:
        - _body_truth [ [[[x1, y1], [x2, y2]], [[x1, y1], [x2, y2]], ... ], ... ] : list of source vectors to compare to
        - body_test [[[x1, y1], [x2, y2]], [[x1, y1], [x2, y2]], ...] : list of limb vectors (body pose)
    Returns:
        - error_max (float) : max error among the whole set
    """
    max_error = 0
    for body_truth in _body_truth:
        error = simple_pose_error(body_truth, body_test)
        if error > max_error:
            max_error = error
    return max_error