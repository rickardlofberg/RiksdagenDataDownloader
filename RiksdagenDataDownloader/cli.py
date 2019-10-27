#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard libary imports
import argparse

from .riksdagen_client import RiksdagenClient
from . import api


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Retrive the data from data.riksdagen.se")

    parser.add_argument(
        '--available-formats',
        default=False,
        help='Print out the available data formats',
        action='store_true')

    parser.add_argument(
        '--format',
        help='Specify the data format to download')

    parser.add_argument(
        '--available-collections',
        default=False,
        help='Print out the available collections',
        action='store_true')

    parser.add_argument(
        '--collection',
        help='Specify the collection to download. Default: all of them')

    parser.add_argument(
        '--dir',
        help='Directory to store output to')

    args = parser.parse_args()

    client = RiksdagenClient()

    if args.available_formats:
        print("Available formats:")
        for available in client.available_formats():
            print(available)

    if args.available_collections:
        print("Available collections:")
        for available in client.available_collections():
            print(available)

    data_format = args.format
    collection = args.collection
    directory = args.dir

    if data_format:
        if args.dir:
            api.download_and_save(data_format, directory, collection)
        else:
            for document in api.download_and_yield(data_format, collection):
                print(document)
