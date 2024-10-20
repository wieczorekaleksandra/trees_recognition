from openimages.download import download_dataset
from multiprocessing import freeze_support

def main():
    download_dataset(
    class_labels=['Tree', 'Plant'],
    annotation_format='darknet',  
    limit=10000,
    dest_dir='open-images-dataset',
    csv_dir='open-images-dataset-csv'
    )

if __name__ == '__main__':
    freeze_support()  # jeżeli to nie windows to może być niepotrzebne
    main()
