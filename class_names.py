import os
import json


from dotenv import load_dotenv
load_dotenv()

PATH_TO_PLANTNET_300K = os.environ.get('PATH_TO_PLANTNET_300K')
base_dir = f'{PATH_TO_PLANTNET_300K}/test'
json_file = f'{PATH_TO_PLANTNET_300K}/../plantnet300K_species_id_2_name.json'
output_file = 'json_plants.json'

def get_species_names_from_folders(base_dir, json_file):
    # Load species data from the JSON file
    with open(json_file, 'r') as f:
        species_data = json.load(f)
    folder_to_species = {}

    # Iterate over folders in the base directory
    class_counter = 0
    for folder_name in os.listdir(base_dir):
        class_counter+=1
        folder_path = os.path.join(base_dir, folder_name)
        
        # Only process if it is a directory and the name matches a species ID
        if os.path.isdir(folder_path) and folder_name in species_data:
            # Get the species name from the JSON data
            species_name = species_data[folder_name]
            folder_to_species[class_counter] = (species_name,class_counter)
        else:
            print(f"Folder {folder_name} does not match a known species ID.")
    
    with open(output_file, 'w') as out_f:
        json.dump(folder_to_species, out_f, indent=4)
    return folder_to_species

get_species_names_from_folders(base_dir, json_file)

