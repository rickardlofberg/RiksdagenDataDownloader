from dataset_retriver import RiksDatasetInterface
import unzip
import requests
import os

def get_dataset_info():
    """ Returns a RiksDatasetInterface to explore the
    avilable datasets """
    return RiksDatasetInterface()

def download_dataset(url, directory, unzipper=unzip):
    """ Download a dataset and save it to path. """
    # Download the data
    data = requests.get(url)

    # Escape if URL is wrong 
    if not data.ok:
        return None

    # Unzip and save file
    return unzipper.save_zip_content(data.content, directory)

def download_documents(self, document_type, data_format, path):
    pass

def download_all_data(data_format, path, interface=RiksDatasetInterface()):
    """ Download all the available data, extract and save it to path.
    The data is saved into subfolders corresponding to 'samling' """

    # Make sure format is available
    if data_format not in interface.available_formats():
        return None

    # Get all datasets (URLs) with correct formatn
    datasets = interface.available_datasets(data_format)

    for dataset in datasets:
        # complete URL is needed to get data
        dataset_url = interface.base_url + dataset
        # This is used to save the data into a folder coresponding to samling
        folder = interface.dataset_info(dataset)['samling']

        # Create an individual path for each dataset
        dataset_path = os.path.join(path, folder)
        
        # Download the dataset
        download_dataset(dataset_url, dataset_path)

def download_to_database(url, db_name, path):
    pass


