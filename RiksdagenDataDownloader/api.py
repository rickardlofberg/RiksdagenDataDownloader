from dataset_retriver import RiksDatasetInterface
import unzip
import requests
import os
import sqlite3
from sql_feeder import SQL_Feeder
import re

def get_dataset_info():
    """ Returns a RiksDatasetInterface to explore the
    avilable datasets """
    return RiksDatasetInterface()

def download_dataset(url, directory, unzipper=unzip, verbose=False):
    """ Download a dataset and save it to path. """
    # Download the data
    data = requests.get(url)

    # Escape if URL is wrong 
    if not data.ok:
        return None

    if verbose:
        print("Retriving file went well..")

    # Unzip and save file
    unzipper.save_zip_content(data.content, directory, verbose=verbose)

def download_and_sql(url, unzipper=unzip, verbose=False):
    """ Download a SQL dataset and yields the data from it. """
    # Download the data
    data = requests.get(url)

    # Escape if URL is wrong 
    if not data.ok:
        return None

    if verbose:
        print("Retriving file went well..")

    # yield a little bit at a time
    # Male sure that this works
    for sql in unzipper.yield_zip_content( data.content, verbose ):
        yield sql

def download_documents(document_type, data_format, path, interface=RiksDatasetInterface()):
    """ Download all the documents of a certain format, and type to a path. """
    # Get the correct documents
    for url in interface.get_document_uri(data_format, document_type):
        # Download one URL at a time
        download_dataset(url, path, verbose=False)

    
def download_all_data(data_format, path, interface=RiksDatasetInterface(), verbose=True):
    """ Download all the available data, extract and save it to path.
    The data is saved into subfolders corresponding to 'samling' """

    # Make sure format is available
    if data_format not in interface.available_formats():
        return None

    # Get all datasets (URLs) with correct formatn
    datasets = interface.available_datasets(data_format)

    if verbose:
        print("Retrived all the datasets with format {}".format(data_format))

    for dataset in datasets:
        # complete URL is needed to get data
        dataset_url = interface.base_url + dataset
        # This is used to save the data into a folder coresponding to samling
        folder = interface.dataset_info(dataset)['samling']

        # Create an individual path for each dataset
        dataset_path = os.path.join(path, folder)
        
        # Download the dataset
        download_dataset(dataset_url, dataset_path, verbose=True)

def download_all_to_database(db_name, path, interface=RiksDatasetInterface(), verbose=False):

    # Path to DB
    db_path = os.path.join(path, db_name)

    # Connect to DB
    conn = sqlite3.connect(db_path)
    db_cursor = conn.cursor()

    # Create sql feeder
    feeder = SQL_Feeder()
    
    """ Should this be another method? """
    # Try creating tables
    #with open(, 'r') as tables:
    for command in feeder.file_feed('../sql/create_tables.sql'):
        try:
            db_cursor.execute(command)
        except:
            print(command)
            print("Error")
            continue

    # Commit all the tables
    conn.commit()
    
    # Create/check database

    # Get SQL datasets
    datasets = interface.available_datasets('sql')
    # Go through each dataset
    for dataset in datasets:
        dataset_url = interface.base_url + dataset
        print(dataset_url)
        for block in download_and_sql(dataset_url, verbose=verbose):
            for sql in feeder.string_feed(block):
                # Make sure it goes well
                try:
                    db_cursor.execute(sql)
                except:
                    print("Error with the SQL string, writing sql string to errors.txt")
                    with open('errors.txt', 'w') as er:
                        print(sql, file=er)
                        print("", file=er)
                
        if verbose:
            print("Commiting {} to database".format(dataset))
            print()
        conn.commit()
