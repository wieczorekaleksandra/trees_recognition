from ultralytics import YOLO


from ultralytics import YOLO
from multiprocessing import freeze_support

def train_model():
        # Load the trained YOLOv8 model (change the path to your trained model file)
    model = YOLO('yolov8n.pt')

    # Evaluate the model on the validation set
    metrics = model.val(data='model_params.yaml', split='val')

    # Print the metrics
    print(metrics.mean_results())
    # Print other metrics

if __name__ == '__main__':
    freeze_support()  # jeżeli to nie windows to może być niepotrzebne
    train_model()
