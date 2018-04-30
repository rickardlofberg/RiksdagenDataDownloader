import zipfile, io, os

def yield_zip_content( request_content, verbose=False):
    """ Returns the raw data as a string from requests object
    which is a zipfile. """
    # Request_content would be the same as request_obj.content
    content = request_content

    # Read the Bytes into a ZipFile-Object
    zipdata = zipfile.ZipFile(io.BytesIO(content))

    # Get all the files in zipfile
    files = zipdata.namelist()

    # Go through each zipped file
    for zipped_file in files:
        # Print out the name of zipfile
        if verbose:
            print("Unpacking {}".format(zipped_file))
        
        # Read the bytes in that file
        byte_data = io.BytesIO(zipdata.read(zipped_file))

        # To save the data as text in 
        text_data = ''

        # Read all the lines in the data
        for line in byte_data:
            # Decode to UTF-8
            text_data += line.decode('utf-8')

        # Yield the data for each zipped file one at a time
        yield text_data

def save_zip_content(request_content, directory='', verbose=False):
    """ Saves the content of the zipfile to path """

    # Make sure we have the directory to save to
    if not os.path.exists(directory):
        os.makedirs(directory)
        if verbose:
            print("Created directory: {}".format(directory))

    # Read the Bytes into a ZipFile-Object
    zipdata = zipfile.ZipFile(io.BytesIO(request_content))

    if verbose:
        print("Starting to extract zipfiles")
    
    # There can be more than one file ...
    for file_name in zipdata.namelist():
        

        # Extract the file
        zipdata.extract(file_name, path=directory)

    if verbose:
        print("Extraction complete")
