#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Third-party imports...
import requests

# Local imports
from . import unzip as unzip
from .riksdagen_client import RiksdagenClient


def uri_generator(data_format, collection=''):
    client = RiksdagenClient()
    return client.get_collection_uri(data_format, collection)


def download_and_yield(data_format, collection=''):
    for url in uri_generator(data_format, collection=''):
        data = requests.get(url)
        for document in unzip.yield_zip_content(data.content):
            yield document


def download_and_save(data_format, path, collection=''):
    client = RiksdagenClient()

    collections = [collection]
    if not collection:
        collections = client.available_collections()

    for collection in collections:
        for url in uri_generator(data_format, collection):
            data = requests.get(url)
            unzip.save_zip_content(data.content, path, collection)
