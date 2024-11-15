import torch
from torchvision.models import resnet152, ResNet152_Weights
import torchvision.transforms as transforms
from PIL import Image
import os
import torch.nn.functional as F
import json

def load_model(model_path, num_classes):
    model = resnet152(weights=ResNet152_Weights.DEFAULT)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))
    model.eval()  
    return model

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_image(image):
    image = transform(image).unsqueeze(0)
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

def use_resnet_model_predict(image):
    model_path = "trained_model3.pth"
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = load_model(model_path,152)
    image_tensor = load_image(image)
    predicted_class = predict_image(model, image_tensor, device, 10)
    with open("json_plants.json", 'r') as f:
        class_to_species = json.load(f)
    print(predicted_class)
    species_name = class_to_species[str(predicted_class[0])]
    print(f'Predicted class: {species_name[0]}')
    return predicted_class[1],species_name[0]
