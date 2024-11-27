import os
import shutil

def collect_photos(source_dir, destination_dir):
    """
    Collects one photo from each subfolder in source_dir, renames it to [id].[file_type],
    and moves it to destination_dir.
    
    Args:
        source_dir (str): The directory containing folders named with IDs.
        destination_dir (str): The directory where renamed photos will be stored.
    """
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)
    
    # Iterate over all folders in the source directory
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        
        # Ensure it's a directory
        if os.path.isdir(folder_path):
            # Get the first file in the directory
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                
                # Check if it's a file
                if os.path.isfile(file_path):
                    # Get the file extension
                    file_extension = os.path.splitext(file_name)[1]
                    
                    # Create the new file name as [id].[file_type]
                    new_file_name = f"{folder_name}{file_extension}"
                    new_file_path = os.path.join(destination_dir, new_file_name)
                    
                    # Copy the file to the destination with the new name
                    shutil.copy(file_path, new_file_path)
                    print(f"Copied: {file_path} -> {new_file_path}")
                    break  # Process only one file per folder

# Example usage
source_directory = r"G:\inzynierka-pliki\plantnet_300K\plantnet_300K\images\test"  # Replace with your source directory path
destination_directory = "./plants"  # Replace with your destination directory path

collect_photos(source_directory, destination_directory)
