#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard library imports
import logging

# Third-party imports...
import xmltodict
import requests


class RiksdagenClient:
    """ A class which acts as an interface to get URIs for the
    available datasets. It does this by downloading and parse
    an XML provided by riksdagen. The class will automatically
    be initilized with a link to an URL.
    Dataset URL last checked: 2018-03-11
    If it doesn't work you can initilize the class with another
    URI.
    """

    def __init__(self, xml_url='http://data.riksdagen.se/dataset/katalog/dataset.xml'):
        self.base_url = 'http://data.riksdagen.se'
        self.documents = dict()

        # Get the metadata and return xmltodict object
        xml_dict = self._get_meta_data(xml_url)
        self._parse_data(xml_dict)

    def __str__(self):
        pass

    def _get_meta_data(self, xml_url):
        """ Helper method to retrive the XML with meta data """
        xml_data = requests.get(xml_url)

        if xml_data:
            xml_dict = xmltodict.parse(xml_data.content, encoding='utf-8')
            return xml_dict
        else:
            logging.critical("Not able to retrive data about the dataset")

    def _parse_data(self, xml_dict):
        """ Helper method to parse the data into new dictionaries"""
        for dataset in xml_dict['datasetlista']['dataset']:
            try:
                doc_format = dataset['format']
                doc_collection = dataset['typ']
                doc_url = dataset['url']

                self.documents[doc_format] = self.documents.get(doc_format, {})
                self.documents[doc_format][doc_collection] = self.documents[doc_format].get(doc_collection, []) + [doc_url]
            except Exception:
                logging.warning(f"Could not parse dataset {dataset}")

    def available_formats(self):
        """ Returns a list of all the available data formats """
        return list(self.documents.keys())

    def available_collections(self):
        """ Returns a list of all the available documenttypes """
        collections = []
        for collection_to_doc in self.documents.values():
            collections = [c for c in collection_to_doc.keys() if c not in collections]
        return collections

    def get_collection_uri(self, data_format, collection=''):
        """ Yield all the URIs to all the available datasets of that type
        and collection. Default is to yield for all collections"""
        try:
            collections = self.documents[data_format]
        except KeyError as key:
            logging.exception(f"{data_format} is an invalid format")
            raise key

        if collection:
            try:
                uris = collections[collection]
            except KeyError:
                logging.exception(f"{collection} is an not a valid collection")
        else:
            uris = [self.base_url + uri for uris in collections.values() for uri in uris]

        for uri in uris:
            yield uri

    def get_collection_uri_and_collection(self, data_format, collection=''):
        """ Yield all the URIs to all the available datasets of that type
        and collection. Default is to yield for all collections"""
        try:
            collections = self.documents[data_format]
        except KeyError as key:
            logging.exception(f"{data_format} is an invalid format")
            raise key

        if collection:
            try:
                uris = collections[collection]
            except KeyError:
                logging.exception(f"{collection} is an not a valid collection")
        else:
            uris = [self.base_url + uri for uris in collections.values() for uri in uris]

        for uri in uris:
            yield uri