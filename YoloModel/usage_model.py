from ultralytics import YOLO

model = YOLO("best.pt")

results = model(source="image.png", show=True, conf=0.25, save=True)
print("Bounding boxes of all detected objects in xyxy format:")
for r in results:
  print(r.boxes.xyxy)

print("Confidence values of all detected objects:")
for r in results:
  print(r.boxes.conf)

print("Class values of all detected objects:")
for r in results:
  print(r.boxes.cls)