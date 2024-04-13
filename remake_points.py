import os
import sys
import cv2
import csv
import argparse
from ultralytics import YOLO

argparser = argparse.ArgumentParser(description='Pose Estimation')
argparser.add_argument('--video', type=str, help='Input Video Path', required=True)
argparser.add_argument('--input', type=str, help='File to input from', default="output.csv", required=False)

#expects constant frame size
#expects constant frame rate

def main(args):
  # Initialize Pose Estimation model
   # Open the video
  # cap = cv2.VideoCapture(0)
  cap = cv2.VideoCapture(args.video)
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))
  norm_box_size = 250
  norm_box = [(frame_width - norm_box_size) // 2, (frame_height - norm_box_size) // 2, (frame_width + norm_box_size) // 2, (frame_height + norm_box_size) // 2]
  represent_box_width = 250

  rows = csv.reader(open(args.input))
  # print(type(rows))
  next(rows)

  # Process each frame
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break

    row = next(rows)
    if row == []:
      row = next(rows)
    # print(row)
    right_arm_start = [int(row[0]), int(row[1])]
    right_arm_end = [int(row[2]), int(row[3])]
    left_arm_start = [int(row[4]), int(row[5])]
    left_arm_end = [int(row[6]), int(row[7])]
    right_leg_start = [int(row[8]), int(row[9])]
    right_leg_end = [int(row[10]), int(row[11])]
    left_leg_start = [int(row[12]), int(row[13])]
    left_leg_end = [int(row[14]), int(row[15])]
    body = [right_arm_start, right_arm_end, left_arm_start, left_arm_end, right_leg_start, right_leg_end, left_leg_start, left_leg_end]
    visible = [i for i in range(len(body)) if body[i][0] != 0 and body[i][1] != 0]
    for limb in body:
      if limb[0] in visible and limb[1] in visible and limb[2] in visible and limb[3] in visible:
        start = (limb[0], limb[1])
        end = (limb[2], limb[3])
        cv2.line(frame, (limb[0], limb[1]), (limb[2], limb[3]), (0, 0, 255), 2)
        cv2.circle(frame, (limb[0], limb[1]), 5, (0, 255, 0), -1)
        cv2.circle(frame, (limb[2], limb[3]), 5, (0, 255, 0), -1)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

if __name__ == '__main__':
    args = argparser.parse_args()
    main(args)