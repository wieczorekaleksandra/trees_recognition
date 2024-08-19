import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, Subset
from torchvision.models import resnext50_32x4d, ResNeXt50_32X4D_Weights

def main():
    selected_classes = ['1355868', '1355920', '1355932'] 
    
    transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    def filter_dataset(dataset, classes):
        class_indices = [dataset.class_to_idx[cls] for cls in classes]
        filtered_indices = [i for i, (_, label) in enumerate(dataset) if label in class_indices]
        return Subset(dataset, filtered_indices)


    train_dataset = ImageFolder(root=r'G:/inzynierka-pliki/plantnet_300K/plantnet_300K/images/train_temp', transform=transform)
    test_dataset = ImageFolder(root=r'G:/inzynierka-pliki/plantnet_300K/plantnet_300K/images/test_temp', transform=transform)

    filtered_train_dataset = filter_dataset(train_dataset, selected_classes)
    filtered_test_dataset = filter_dataset(test_dataset, selected_classes)

    train_loader = DataLoader(filtered_train_dataset, batch_size=16, shuffle=True, num_workers=4, pin_memory=True)
    test_loader = DataLoader(filtered_test_dataset, batch_size=16, shuffle=False, num_workers=4, pin_memory=True)

    num_classes = len(selected_classes)

    model = resnext50_32x4d(weights=ResNeXt50_32X4D_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=5e-4)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

    num_epochs = 10  

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        scheduler.step()

        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')

        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        print(f'Accuracy of the model on the test images: {100 * correct / total:.2f}%')

    print('Finished Training')
if __name__ == '__main__':
    main()
