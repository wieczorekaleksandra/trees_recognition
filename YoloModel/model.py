from ultralytics import YOLO
from multiprocessing import freeze_support

def train_model():
    model = YOLO('yolov8n.pt')
    model.train(data='model_params.yaml', epochs=100)  

if __name__ == '__main__':
    freeze_support()  
    train_model()
