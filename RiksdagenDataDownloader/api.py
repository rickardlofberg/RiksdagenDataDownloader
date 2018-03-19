"""
This is the functionality I strive for:

import RiksdagenDataDownloader as rdd
datasets = rdd.get_datasets()
rdd.download_dataset()
rdd.download_all_data()
rdd.download_to_database()
"""


def get_datasets():
    """ Returns a RiksDatasetInterface to explire the
    avilable datasets """
    return RiksDatasetInterface()

def download_dataset():
    pass

def download_all_data():
    pass

def download_to_database():
    pass


