import torch
from torchvision.models import resnet18, ResNet18_Weights
import torchvision.transforms as transforms
from PIL import Image
import os
import torch.nn.functional as F

def load_model(model_path, num_classes):
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))
    model.eval()  
    return model

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_image(image_path):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add batch dimension
    return image

def predict_image(model, image_tensor, device, selected_classes):
    image_tensor = image_tensor.to(device)
    model = model.to(device)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = F.softmax(outputs, dim=1)  
        confidence, predicted = torch.max(probabilities, 1)    
        
    predicted_class = predicted.item()
    certainty = confidence.item()  
    
    print(f'Predicted class (number from the used classes): {predicted_class}, Certainty: {certainty:.4f}')
    return predicted_class, certainty

if __name__ == '__main__':
    model_path = "trained_model3.pth"
    image_path = "YoloModel/image.png"
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = load_model(model_path,193)
    image_tensor = load_image(image_path)
    predicted_class = predict_image(model, image_tensor, device, 10)
    
    print(f'Predicted class: {predicted_class}')
