import os
import sys
from pathlib import Path
from ultralytics import YOLO

#YOLOv8 nano
model = YOLO("yolov8n.pt")

frames_path = os.environ.get("CONF_FRAMES_DIR")

if not frames_path or not os.listdir(frames_path):
    raise ValueError("ERROR: vision.py frame reading")

#Sort and glob in case of missed frames
frames = sorted(Path(frames_path).glob("frame_*.jpg"))

#Skipping frames for speed
MAX_FRAMES = 10
if len(frames) > MAX_FRAMES:
    step = len(frames) // MAX_FRAMES
    frames = frames[::step]

results = model(source=frames, imgsz=480, batch=4, conf=0.5)

#YOLO human class = 0
human_class_id = 0

#Records max humans found
max_humans = 0
for r in results:
    humans = sum(1 for x in r.boxes if x.cls == human_class_id)
    if humans > max_humans:
        max_humans = humans

#Propogation
print(max_humans)
sys.exit(0) 
