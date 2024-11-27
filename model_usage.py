import cv2
from PIL import Image
import time 
from ultralytics import YOLO
from pathlib import Path
import numpy as np
import sys
from resnet_usage import use_resnet_model_predict 


def process_image(input_image):
    plant_filenames=[]
    model = YOLO("best.pt")
    detections = model(input_image)

    trees = detections[0].boxes.data.cpu().numpy()
    list_of_detected_plant=[]
    for i, box in enumerate(trees):
        x1, y1, x2, y2, conf, cls = box
        plant_cropped = input_image.crop((x1, y1, x2, y2))
        plant_filename = f'plant_{i}.jpg'
        plant_cropped.save(plant_filename)
        plant_filenames.append(plant_cropped)
        detected_plant = use_resnet_model_predict(plant_cropped)
        list_of_detected_plant.append(detected_plant)
        print(f"Plant {i+1} ")
    if len(trees) == 0:
        list_of_detected_plant.append(use_resnet_model_predict(input_image))
    return list_of_detected_plant
