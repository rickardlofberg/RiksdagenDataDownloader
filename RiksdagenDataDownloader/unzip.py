#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard library imports
import io
import os
import zipfile


def yield_zip_content(request_content):
    """ Returns the raw data as a string from requests object
    which is a zipfile. """
    # Read the Bytes into a ZipFile-Object
    zipdata = zipfile.ZipFile(io.BytesIO(request_content))

    for zipped_file in zipdata.namelist():
        yield zipdata.read(zipped_file).decode('utf-8')


def save_zip_content(request_content, directory='', subfolder=''):
    """ Saves the content of the zipfile to path. """
    # Make sure we have the directory to save to
    if not os.path.exists(directory):
        raise Exception("Selected folder doesn't exists.")

    if subfolder:
        directory = os.path.join(directory, subfolder)
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Read the Bytes into a ZipFile-Object
    zipdata = zipfile.ZipFile(io.BytesIO(request_content))

    for file_name in zipdata.namelist():
        zipdata.extract(file_name, path=directory)
