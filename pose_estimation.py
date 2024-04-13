import cv2
import argparse
from ultralytics import YOLO

# Form limb vectors from video file or webcam

argparser = argparse.ArgumentParser(description='Pose Estimation using YOLOv5')
argparser.add_argument('--source', type=str, default='0', help='source')  # file/folder, 0 for webcam

def main(args):
  #init model
  model = YOLO('models/yolov8n-pose')

  if args.source == '0':
    args.source = 0
  #start source capture
  cap = cv2.VideoCapture(args.source)
  #get frame dimensions
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  norm_box_size = 250
  #get normalized (centered) box coordinates
  norm_box = [(width - norm_box_size) // 2, (height - norm_box_size) // 2, (width + norm_box_size) // 2, (height + norm_box_size) // 2]

  #limbs
  right_arm = [6, 10]
  left_arm = [5, 9]
  left_leg = [12, 14]
  right_leg = [11, 13]
  body = [right_arm, left_arm, right_leg, left_leg]

  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    #detect objects
    results = model(frame, show=False, verbose=False)
    #get keypoints
    keypoints = results[0].keypoints.xy[0]
    #get bounding box
    try:
      box = results[0].boxes.xyxy[0]
    except:
      box = [0, 0, 0, 0]
    #output bounding box
    cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)

    # Show the keypoints
    visible = [i for i in range(keypoints.shape[0]) if keypoints[i][0] != 0 and keypoints[i][1] != 0]
    for limb in body:
      if limb[0] in visible and limb[1] in visible:
        start = keypoints[limb[0]]
        end = keypoints[limb[1]]
        cv2.line(frame, (int(start[0]), int(start[1])), (int(end[0]), int(end[1])), (255, 0, 0), thickness=1)
        cv2.circle(frame, (int(start[0]), int(start[1])), radius=3, color=(0, 255, 0), thickness=2)
        cv2.circle(frame, (int(end[0]), int(end[1])), radius=3, color=(0, 0, 255), thickness=2)

    #draw normalized box
    cv2.rectangle(frame, (norm_box[0], norm_box[1]), (norm_box[2], norm_box[3]), (102, 51, 153), 2)
    #display frame
    cv2.imshow('frame', frame)
    #exit on q
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

if __name__ == '__main__':
  args = argparser.parse_args()
  main(args)