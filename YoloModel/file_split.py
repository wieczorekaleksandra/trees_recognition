import os
import random
import shutil

# Paths
dataset_path = 'G:/Repo-inzynier/trees_recognition/YoloModel/open-images-dataset/plant'
images_path = os.path.join(dataset_path, 'images')
labels_path = os.path.join(dataset_path, 'darknet')

os.makedirs(os.path.join(images_path, 'train'), exist_ok=True)
os.makedirs(os.path.join(images_path, 'val'), exist_ok=True)
os.makedirs(os.path.join(labels_path, 'train'), exist_ok=True)
os.makedirs(os.path.join(labels_path, 'val'), exist_ok=True)

# List all image files
image_files = [f for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')]
random.shuffle(image_files)

# Split ratio
split_ratio = 0.8
split_index = int(len(image_files) * split_ratio)

# Split into train and val
train_files = image_files[:split_index]
val_files = image_files[split_index:]

# Function to move files
def move_files(file_list, split_type):
    for file_name in file_list:
        # Move images
        src_image_path = os.path.join(images_path, file_name)
        dest_image_path = os.path.join(images_path, split_type, file_name)
        shutil.move(src_image_path, dest_image_path)
        
        # Move corresponding label files
        label_file = file_name.replace('.jpg', '.txt').replace('.png', '.txt')
        src_label_path = os.path.join(labels_path, label_file)
        dest_label_path = os.path.join(labels_path, split_type, label_file)
        
        if os.path.exists(src_label_path):
            shutil.move(src_label_path, dest_label_path)

# Move the files
move_files(train_files, 'train')
move_files(val_files, 'val')

print("Data split complete!")
