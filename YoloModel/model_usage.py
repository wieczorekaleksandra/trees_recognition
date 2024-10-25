import cv2
from PIL import Image
import time 
from ultralytics import YOLO
from pathlib import Path
import numpy as np
import sys
sys.path.append('../')
from resnet_usage import use_resnet_model_predict 


def process_image(image_path):
    plant_filenames=[]
    model = YOLO("best.pt")
    input_image = Image.open(image_path)
    detections = model(input_image)

    trees = detections[0].boxes.data.cpu().numpy()

    for i, box in enumerate(trees):
        x1, y1, x2, y2, conf, cls = box
        plant_cropped = input_image.crop((x1, y1, x2, y2))
        plant_filename = f'plant_{i}.jpg'
        plant_cropped.save(plant_filename)
        plant_filenames.append(plant_cropped)
        use_resnet_model_predict(plant_cropped)
        print(f"Plant {i+1} ")
