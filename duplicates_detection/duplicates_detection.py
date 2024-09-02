import os
from PIL import Image
import imagehash
import shutil

from dotenv import load_dotenv
load_dotenv()

PATH_TO_PLANTNET_300K = os.environ.get('PATH_TO_PLANTNET_300K')
image_dir_train = os.path.join(PATH_TO_PLANTNET_300K, 'images/train')
image_dir_test = os.path.join(PATH_TO_PLANTNET_300K, 'images/test')


hashes = {}
duplicates = []

def find_duplicates(image_dir_train):
    dir_number = 0
    # Loop through all directories in the train directory
    for selected_class in os.listdir(image_dir_train):
        class_dir = os.path.join(image_dir_train, selected_class)
        class_dir_test = os.path.join(image_dir_test, selected_class)

        if not os.path.isdir(class_dir):
            continue  # Skip if it's not a directory
        
        file_count = len([name for name in os.listdir(class_dir) if name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
        print(f"Number of files in directory {selected_class} : {file_count}")
        if file_count < 200: 
            try:
                shutil.rmtree(class_dir_test)
                shutil.rmtree(class_dir)
                print(f"Deleted directory: {selected_class}")
            except Exception as e:
                print(f"Error deleting directory {selected_class}: {e}")
            continue 

        dir_number += 1
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
                    #Image.open(os.path.join(class_dir, hashes[img_hash])).show()
                    #Image.open(filepath).show()
                else:
                    hashes[img_hash] = filename
    print(f"Number of directories in train {dir_number}")

find_duplicates(image_dir_train)

if duplicates:
    print(f"Total number of duplicates found: {len(duplicates)}")
    print("Found duplicates:")
    for dup in duplicates:
        print(f"Duplicate in class {dup[2]}: {dup[0]} - Original: {dup[1]} - Deleting duplicate")
        duplicate_path = os.path.join(image_dir_train, dup[2], dup[0])
        try:
            os.remove(duplicate_path)
            print(f"Deleted duplicate file: {dup[0]}")
        except Exception as e:
            print(f"Error deleting {dup[0]}: {e}")
else:
    print("No duplicates found.")
