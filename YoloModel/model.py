from ultralytics import YOLO
from multiprocessing import freeze_support

def train_model():
    model = YOLO('yolov8n.yaml')  # Load your model
    model.train(data='model_params.yaml', epochs=100)  # Start training

if __name__ == '__main__':
    freeze_support()  # jeżeli to nie windows to może być niepotrzebne
    train_model()
