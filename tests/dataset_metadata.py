#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard library imports 
import xml.etree.cElementTree as ET
import datetime
import logging
import uuid

# Third party libs
from faker import Faker
from faker.providers import address, date_time

logging.disable(logging.DEBUG)

fake = Faker('en_GB')
fake.add_provider(address)
fake.add_provider(date_time)


def xml_metadata(number_of_datasets=1, set_format=None, set_collection=None):
    root = ET.Element("datasetlista")

    datatypes = ['xml', 'json', 'zip', 'html', 'sql', 'csv', 'text']
    collections = ['anforande', 'bet', 'ds', 'EUN', 'f-lista', 'fpm', 'frsrdg', 'ip', 'kammakt', 'mot', 'Övrigt', 'prop', 'prot', 'Riksdagens diarium', 'rskr', 'samtr', 'Skriftliga frågor', 'sou', 't-lista', 'Utredningar', 'utskottsdokument', 'yttr', 'Ledamotsdata', 'votering']

    for _ in range(number_of_datasets):
        collection = set_collection or fake.random_element(elements=collections)
        
        start_date = datetime.date(year=1993, month=1, day=1)
        date = fake.date_time_between_dates(datetime_start=start_date)
        fake_date = '{:%Y-%m-%d %X}'.format(date)
        yyyy_slash_yy = '{}/{}'.format(date.year, str(date.year+1)[-2:])
        yyyy_yy = '{}{}'.format(date.year, str(date.year+1)[-2:])
        collection_date = '{}-{}'.format(collection, yyyy_slash_yy)

        data_format = set_format or fake.random_element(elements=datatypes)
        file_format = 'zip'
        file_name = '{}-{}.{}.{}'.format(collection, yyyy_yy, data_format, file_format)
        url = '/dataset/anforande/{}'.format(file_name)

        doc = ET.SubElement(root, "dataset")
        ET.SubElement(doc, 'namn').text = '{}'.format(collection)
        ET.SubElement(doc, 'typ').text = '{}'.format(collection)
        ET.SubElement(doc, 'samling').text = '{}'.format(collection_date)
        ET.SubElement(doc, 'rm').text = '{}'.format(yyyy_slash_yy)
        ET.SubElement(doc, 'filnamn').text = '{}'.format(file_name)
        ET.SubElement(doc, 'storlek').text = '{}'.format(fake.random_int(min=1000, max=3000000))
        ET.SubElement(doc, 'format').text = '{}'.format(data_format)
        ET.SubElement(doc, 'filformat').text = '{}'.format(file_format)
        ET.SubElement(doc, 'uppdaterad').text = '{}'.format(fake_date)
        ET.SubElement(doc, 'url').text = '{}'.format(url)
        ET.SubElement(doc, 'description').text = '{}'.format(fake.text())
        ET.SubElement(doc, 'upplysning').text = '{}'.format(fake.text())

    return ET.tostring(root,encoding='utf8', method='xml')
