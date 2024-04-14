from ultralytics import YOLO
from choreography import Choreography
import dance_comparison as dc

class DanceError():
  def __init__(self, dance: Choreography):
    self.dance = dance
    self.name = dance.name
    self.csv_path = dance.csv_path
    self.mp4_path = dance.mp4_path
    self.icon_path = dance.icon_path
    self.threshold = dance.threshold
    self.above_ratio = dance.above_ratio
    self.below_ratio = dance.below_ratio
    self.temporal_size = dance.temporal_size
    self.sma_window = dance.sma_window
    self.min_error = dance.min_error
    self.max_error = dance.max_error
    self.score_timing = dance.score_timing

    self.score = 0
    self.model = YOLO("./models/yolov8n-pose.pt")

  def get_score(self, webcam_frame):
    return dc.dance_comparison(self.dance, webcam_frame, {})