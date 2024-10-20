from ultralytics import YOLO


from ultralytics import YOLO
from multiprocessing import freeze_support

def train_model():
    model = YOLO('yolov8n.pt')
    metrics = model.val(data='model_params.yaml', split='val')
    print(metrics.mean_results())

if __name__ == '__main__':
    freeze_support() 
    train_model()
