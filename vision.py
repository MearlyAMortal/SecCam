import os
import sys
from pathlib import Path
from ultralytics import YOLO

#YOLOv8 nano
model = YOLO("yolov8n.pt")
#model = YOLO("yolov8n_int8.pt")

frames_path = os.environ.get("CONF_FRAMES_DIR")

if not frames_path or not os.listdir(frames_path):
    raise ValueError("ERROR: vision.py frame reading")

#Sort and glob in case of missed frames
all_frames = sorted(Path(frames_path).glob("frame_*.jpg"))[:90]

#Skipping frames for speed
STEP = 6
frames = all_frames[::STEP]

results = model.predict(
	source=frames,
	imgsz=320,
	batch=16,
	conf=0.5,
	stream=True
)

#YOLO human class = 0
human_class_id = 0

#Records max humans found
max_humans = 0
for r in results:
    humans = sum(1 for x in r.boxes if int(x.cls) == human_class_id)
    if humans > max_humans:
        max_humans = humans

#Propogation
print(max_humans)
sys.exit(0) 
