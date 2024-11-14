import os
import shutil

# Paths to your directories (Windows-compatible)
images_train_dir = r'open-images-dataset\plant\images\train'
images_val_dir = r'open-images-dataset\plant\images\val'
labels_dir = r'open-images-dataset\plant\labels'
output_labels_train_dir = r'open-images-dataset\plant\labels\train'
output_labels_val_dir = r'open-images-dataset\plant\labels\val'

# Create output directories if they don't exist
os.makedirs(output_labels_train_dir, exist_ok=True)
os.makedirs(output_labels_val_dir, exist_ok=True)

# Function to move labels to the correct directory
def move_labels(image_dir, output_labels_dir):
    for image_file in os.listdir(image_dir):
        # Extract the base filename (without extension)
        base_name = os.path.splitext(image_file)[0]
        
        # Find the corresponding label file
        label_file = base_name + '.txt'
        label_path = os.path.join(labels_dir, label_file)
        
        # Check if the label file exists
        if os.path.exists(label_path):
            # Move the label file to the correct directory
            shutil.move(label_path, os.path.join(output_labels_dir, label_file))
        else:
            print(f"Label not found for {image_file}")

# Move labels for training images
move_labels(images_train_dir, output_labels_train_dir)

# Move labels for validation images
move_labels(images_val_dir, output_labels_val_dir)

print("Labels successfully split into train and val sets!")
