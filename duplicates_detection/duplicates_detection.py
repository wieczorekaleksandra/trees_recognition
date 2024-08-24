import os
from PIL import Image
import imagehash

from dotenv import load_dotenv
load_dotenv()

PATH_TO_PLANTNET_300K = os.environ.get('PATH_TO_PLANTNET_300K')
image_dir = os.path.join(PATH_TO_PLANTNET_300K, 'images/train')
selected_classes = ['1356111', '1355868']

hashes = {}
duplicates = []

def find_duplicates(image_dir, selected_classes):
    for selected_class in selected_classes:
        class_dir = os.path.join(image_dir, selected_class) 
        print(f"Checking duplicates in class: {selected_class}")

        for filename in os.listdir(class_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                filepath = os.path.join(class_dir, filename)
                try:
                    img = Image.open(filepath)
                    img_hash = imagehash.phash(img) 
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    continue

                if img_hash in hashes:
                    duplicates.append((filename, hashes[img_hash], selected_class))
                    print(f"Duplicate found in class {selected_class}: {filename} is a duplicate of {hashes[img_hash]}")

                    print(f"Opening original image: {hashes[img_hash]}")
                    Image.open(os.path.join(class_dir, hashes[img_hash])).show()

                    print(f"Opening duplicate image: {filename}")
                    Image.open(filepath).show()
                else:
                    hashes[img_hash] = filename

find_duplicates(image_dir, selected_classes)
 

if duplicates:
    print("Found duplicates:")
    for dup in duplicates:
        print(f"Duplicate in class {dup[2]}: {dup[0]} - Original: {dup[1]}")
else:
    print("No duplicates found.")