import os
import sys
import cv2
import csv
import argparse
from ultralytics import YOLO

argparser = argparse.ArgumentParser(description='Pose Estimation')
argparser.add_argument('--video', type=str, help='Input Video Path', required=True)
argparser.add_argument('--output', type=str, help='File to output to', default="output.csv", required=False)

#expects constant frame size
#expects constant frame rate

def main(args):
  # Initialize Pose Estimation model
  output_file = open(args.output, 'w')
  output_writer = csv.writer(output_file)
  # output_writer.writerow(['right_arm_start_x', 'right_arm_start_y', 'right_arm_end_x', 'right_arm_end_y', 'left_arm_start_x', 'left_arm_start_y', 'left_arm_end_x', 'left_arm_end_y', 'right_leg_start_x', 'right_leg_start_y', 'right_leg_end_x', 'right_leg_end_y', 'left_leg_start_x', 'left_leg_start_y', 'left_leg_end_x', 'left_leg_end_y'])
  output_writer.writerow(['right_upper_arm_start_x', 'right_upper_arm_start_y', 
                          'right_upper_arm_end_x', 'right_upper_arm_end_y', 
                          'right_forearm_start_x', 'right_forearm_start_y', 
                          'right_forearm_end_x', 'right_forearm_end_y', 
                          'left_upper_arm_start_x', 'left_upper_arm_start_y', 
                          'left_upper_arm_end_x', 'left_upper_arm_end_y', 
                          'left_forearm_start_x', 'left_forearm_start_y', 
                          'left_forearm_end_x', 'left_forearm_end_y',
                          'right_quad_start_x', 'right_quad_start_y', 
                          'right_quad_end_x', 'right_quad_end_y', 
                          'right_calf_start_x', 'right_calf_start_y', 
                          'right_calf_end_x', 'right_calf_end_y', 
                          'left_quad_start_x', 'left_quad_start_y', 
                          'left_quad_end_x', 'left_quad_end_y',
                          'left_calf_start_x', 'left_calf_start_y', 
                          'left_calf_end_x', 'left_calf_end_y'])
  model = YOLO('yolov8n-pose')

   # Open the video
  # cap = cv2.VideoCapture(0)
  cap = cv2.VideoCapture(args.video)
  desired_fps = 25
  cap.set(cv2.CAP_PROP_FPS, desired_fps)
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))
  norm_box_size = 250
  norm_box_width = 200
  norm_box_height = 300
  norm_box = [(frame_width - norm_box_width) // 2, 
              (frame_height - norm_box_height) // 2, 
              (frame_width + norm_box_width) // 2, 
              (frame_height + norm_box_height) // 2]
  represent_box_width = 250

  #limbs
  # right_arm = [6, 10]
  # left_arm = [5, 9]
  # left_leg = [12, 14]
  # right_leg = [11, 13]
  # body = [right_arm, left_arm, right_leg, left_leg]

  right_upper_arm = [5, 7]
  right_forearm = [7, 9]
  left_upper_arm = [6, 8]
  left_forearm = [8, 10]
  right_quad = [11, 13]
  right_calf = [13, 15]
  left_quad = [12, 14]
  left_calf = [14, 16]
  body = [right_upper_arm, right_forearm, left_upper_arm, left_forearm, right_quad, right_calf, left_quad, left_calf]

  print("going into try block")

  # Process each frame
  try:
    while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
        break

      print("read from cap")

      # Run model prediction
      results = model(frame, show=False, verbose=False)

      # Access keypoints
      keypoints = results[0].keypoints.xy[0]
      boxes = results[0].boxes

      # Show the frame
      try:
        box = boxes.xyxy[0]
      except:
        box = [0,0,0,0]
      # cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)
      box_start = [int(box[0]), int(box[1])]

      print("drawing keypoints")

      # Show the keypoints
      visible = [i for i in range(keypoints.shape[0]) if keypoints[i][0] != 0 and keypoints[i][1] != 0]
      csv_row = []
      for limb in body:
        if limb[0] in visible and limb[1] in visible:
          start = keypoints[limb[0]]
          end = keypoints[limb[1]]
          norm_start = [int((start[0] - box_start[0]) * represent_box_width / (box[2] - box[0])), int((start[1] - box_start[1]) * represent_box_width / (box[3] - box[1]))]
          norm_end = [int((end[0] - box_start[0]) * represent_box_width / (box[2] - box[0])), int((end[1] - box_start[1]) * represent_box_width / (box[3] - box[1]))]
          csv_row.extend(norm_start)
          csv_row.extend(norm_end)
          cv2.circle(frame, (norm_start[0] + norm_box[0], norm_start[1] + norm_box[1]), radius=3, color=(0, 255, 0), thickness=4)
          cv2.circle(frame, (norm_end[0] + norm_box[0], norm_end[1] + norm_box[1]), radius=3, color=(0, 0, 255), thickness=4)
          cv2.line(frame, (norm_start[0] + norm_box[0], norm_start[1] + norm_box[1]), (norm_end[0] + norm_box[0], norm_end[1] + norm_box[1]), (102, 51, 153), thickness=4)
        else:
          csv_row.extend([0, 0, 0, 0])
      cv2.rectangle(frame, (norm_box[0], norm_box[1]), (norm_box[2], norm_box[3]), (102, 51, 153), 4)
      output_writer.writerow(csv_row)
      cv2.imshow('frame', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print("leaving try")
  except KeyboardInterrupt:
    print("keyboard interrupt!")
    output_file.close()
    cap.release()
  except Exception as e:
    output_file.close()
    cap.release()
    print(f"exception: {e}")

if __name__ == '__main__':
    args = argparser.parse_args()
    main(args)