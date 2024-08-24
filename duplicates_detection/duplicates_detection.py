import os
from PIL import Image
import imagehash

from dotenv import load_dotenv
load_dotenv()

PATH_TO_PLANTNET_300K = os.environ.get('PATH_TO_PLANTNET_300K')
image_dir = os.path.join(PATH_TO_PLANTNET_300K, 'images/train')

hashes = {}
duplicates = []

def find_duplicates(image_dir):
    # Loop through all directories in the train directory
    for selected_class in os.listdir(image_dir):
        class_dir = os.path.join(image_dir, selected_class)
        if not os.path.isdir(class_dir):
            continue  # Skip if it's not a directory

        file_count = len([name for name in os.listdir(class_dir) if name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
        print(f"Number of files in {selected_class} directory: {file_count}")

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
                    duplicates.append((filename, hashes[img_hash], selected_class, file_count))

                    #Image.open(os.path.join(class_dir, hashes[img_hash])).show()
                    #Image.open(filepath).show()
                else:
                    hashes[img_hash] = filename

find_duplicates(image_dir)

if duplicates:
    print(f"Total number of duplicates found: {len(duplicates)}")
    print("Found duplicates:")
    for dup in duplicates:
        if dup[3] > 200:
            print(f"Duplicate in class {dup[2]}: {dup[0]} - Original: {dup[1]} - Deleting duplicate")
            # duplicate_path = os.path.join(image_dir, dup[2], dup[0])
            # try:
            #     os.remove(duplicate_path)
            #     print(f"Deleted duplicate file: {dup[0]}")
            # except Exception as e:
            #     print(f"Error deleting {dup[0]}: {e}")
        else:
            print(f"Duplicate in class {dup[2]}: {dup[0]} - Original: {dup[1]} - Flipping duplicate vertically")
            # duplicate_path = os.path.join(image_dir, dup[2], dup[0])
            # try:
            #     img = Image.open(duplicate_path)
            #     img = img.transpose(Image.FLIP_TOP_BOTTOM)
            #     img.save(duplicate_path)
            #     print(f"Flipped and saved duplicate file: {dup[0]}")
            # except Exception as e:
            #     print(f"Error flipping {dup[0]}: {e}")
else:
    print("No duplicates found.")
