import os
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

image_path = os.environ.get("CONF_IMAGE_DIR")
if not image_path:
    raise ValueError("CONF_IMAGE_DIR not set")


results = model(source=image_path)

# Count humans
human_count = 0
for box in results[0].boxes:
    cls = int(box.cls[0])
    conf = float(box.conf[0])
    if cls == 0 and conf > 0.5:
        human_count += 1

print(f"Humans detected: {human_count}")
