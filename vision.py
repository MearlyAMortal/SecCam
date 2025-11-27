import os
import sys
from pathlib import Path
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

image_path = os.environ.get("CONF_IMAGE_DIR")
frames_path = os.environ.get("CONF_FRAMES_DIR")

if not frames_path or not os.listdir(frames_path):
    raise ValueError("ERROR: vision.py frame reading.")

frames = sorted(Path(frames_path).glob("frame_*.jpg"))

MAX_FRAMES = 10
if len(frames) > MAX_FRAMES:
    step = len(frames) // MAX_FRAMES
    frames = frames[::step]

results = model(source=frames, imgsz=480, batch=4, conf=0.5)

human_class_id = 0
max_humans = 0
for r in results:
    humans = sum(1 for x in r.boxes if x.cls == human_class_id)
    if humans > max_humans:
        max_humans = humans

print(max_humans)
sys.exit(0) 
