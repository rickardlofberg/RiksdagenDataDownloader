import zipfile, io, os

def yield_zip_content( request_content ):
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
        # Read the bytes in that file
        byte_data = io.BytesIO(zipdata.read(zipped_file))

        # To save the data as text in 
        text_data = ''

        # Read all the lines in the data
        while byte_data.readline():
            # Byte to text
            text_data += byte_data.readline().decode('utf-8')

        # Yield the data for each zipped file one at a time
        yield text_data

def save_zip_content( request_content, directory='' ):
    """ Saves the content of the zipfile to path """

    # Make sure we have the directory to save to
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Read the Bytes into a ZipFile-Object
    zipdata = zipfile.ZipFile(io.BytesIO(request_content))
        
    # There can be more than one file ...
    for file_name in zipdata.namelist():
        # Extract the file
        zipdata.extract(file_name, path=directory)
