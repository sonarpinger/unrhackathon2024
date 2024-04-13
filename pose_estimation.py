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
  print(f"{width}x{height}")
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
    cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)

    #display frame
    cv2.imshow('frame', frame)
    #exit on q
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

if __name__ == '__main__':
  args = argparser.parse_args()
  main(args)