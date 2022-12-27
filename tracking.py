from detection_helpers import *
from tracking_helpers import *
from bridge_wrapper import *
from PIL import Image

detector = Detector(classes = [0,1,2]) # it'll detect ONLY [helmet, people, head]. class = None means detect all classes. List info at: "data/coco.yaml"
detector.load_model('/root/helmet_det/yolov7-main/models/best.pt', img_size=2016) # pass the path to the trained weight file

# Initialise  class that binds detector and tracker in one class
tracker = YOLOv7_DeepSORT(reID_model_path="./deep_sort/model_weights/mars-small128.pb", detector=detector)

# output = None will not save the output video
FILE = 'SD_Gate_Cam_1'
tracker.track_video(f"./IO_data/input/video/{FILE}.MP4", output=f"./IO_data/output/SD_Gate_Cam_2.mp4", show_live = False, skip_frames = None, count_objects = True, verbose=1)
