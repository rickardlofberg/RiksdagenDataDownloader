from dataset_retriver import RiksDatasetInterface
import zipextractor as unzip
import requests
import os

def get_dataset_info():
    """ Returns a RiksDatasetInterface to explire the
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
    unzipper.save_zip_content(data.content, directory)

def download_data(self, document_type, data_format, path):
    pass

def download_all_data(data_format, path):
    pass

def download_to_database(url, db_name, path):
    pass


