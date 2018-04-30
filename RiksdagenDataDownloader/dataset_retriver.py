import requests, xmltodict

class RiksDatasetInterface:
    """ A class which acts as an interface to get URIs for the
    available datasets. It does this by downloading and parse
    an XML provided by riksdagen. The class will automatically
    be initilized with a link to an URL.
    Dataset URL last checked: 2018-03-11
    If it doesn't work you can initilize the class with another
    URI.
    """

    def __init__(self, xml_url='http://data.riksdagen.se/dataset/katalog/dataset.xml'):
        # Base url to riksdagen data
        self.base_url = 'http://data.riksdagen.se'
        # Holds datasets according to format
        self.format_dataset = dict()
        # A dictionary which holds info about an URL
        self.url_info = dict()
        
        # Get the metadata and return xmltodict object
        xml_dict = self._get_meta_data(xml_url)

        # If unsucesful
        if xml_dict == None:
            print("Something went wrong when retriving the dataset, make \
            sure the URL is correct.")
        else:
            # Parse data int above dictionaries
            self._parse_data(xml_dict)

    def _get_meta_data(self, xml_url):
        """ Helper method to retrive the XML with meta data """
        # Get the XML file
        data_xml = requests.get(xml_url)
        
        # Make sure we sure we got an OK
        if data_xml.status_code == 200:
            # Change bytes to UTF-8 string
            clean_xml = ''.join([line.decode('utf-8') for line in data_xml.iter_lines()])
            # Create to a xml dict structure
            xml_dict = xmltodict.parse(clean_xml)
            return xml_dict
        return None
            
    def _parse_data(self, xml_dict):
        """ Helper method to parse the data into new dictionaries"""
        try:
            for dataset in xml_dict['datasetlista']['dataset']:
                # Format to URLs
                self.format_dataset[dataset['format']] = \
                self.format_dataset.get(dataset['format'], []) + [dataset['url']]
                # URL represents a dataset, which hold info
                self.url_info[dataset['url']] = dataset
        except:
            print("Something went wrong when parsing the XML file")
            
    def available_formats(self):
        """ Returns a list of all the available data formats """
        return list(self.format_dataset.keys())

    def available_datasets(self, data_format=None ):
        """ Returns a list of all the available datasets for 
        a given data formats """
        # If no specific format given, return all of them
        if not data_format:
            dSets = []
            for dSet in self.format_dataset.keys():
                dSets.extend(self.format_dataset[dSet])
            return dSets
        # Otherwise return the sets for format or  empty list
        else:
            return self.format_dataset.get(data_format, [])

    def available_doc_types(self):
        """ Returns a list of all the available documenttypes """
        doc_types = []
        for dataset in self.available_datasets():
            if self.dataset_info(dataset)['namn'] not in doc_types:
                doc_types.append(self.dataset_info(dataset)['namn'])
        return doc_types

    def dataset_info(self, url):
        """ Returns a dictionary with all the info for dataset """
        return self.url_info.get(url, None)

    def get_all_dataset_uri(self, data_format='sql'):
        """ Yield all the URIs to all the available datasets of that type. """
        for dataset in self.available_datasets(data_format):
            yield self.base_url + dataset
        
    def get_all_dataset_uri_size(self, data_format='sql'):
        """ Yield all the URIs to all the available datasets of that type
        and the size of the dataset as a tuple. """
        for dataset in self.available_datasets(data_format):
            yield (self.base_url + dataset, self.dataset_info(dataset)['storlek'])

    def get_document_uri(self, data_format='sql', datatype=''):
        """ Yield all the URIs for document type anforande. """
        for dataset in self.available_datasets(data_format):
            if datatype == '' or self.dataset_info(dataset)['namn'] == datatype:
                yield self.base_url + dataset            

    # These methods are repetative.
    # It is meant this way to make the interface easier.
    def get_all_anforande_uri(self, data_format='sql'):
        """ Yield all the URIs for document type anforande. """
        for dataset in self.available_datasets(data_format):
            if self.dataset_info(dataset)['namn'] == 'anforande':
                yield self.base_url + dataset

    def get_all_dokument_uri(self, data_format='sql'):
        """ Yield all the URIs for document type dokument. """
        for dataset in self.available_datasets(data_format):
            if self.dataset_info(dataset)['namn'] == 'dokument':
                yield self.base_url + dataset

    def get_all_person_uri(self, data_format='sql'):
        """ Yield all the URIs for document type person. """
        for dataset in self.available_datasets(data_format):
            if self.dataset_info(dataset)['namn'] == 'person':
                yield self.base_url + dataset

    def get_all_votering_uri(self, data_format='sql'):
        """ Yield all the URIs for document type votering. """
        for dataset in self.available_datasets(data_format):
            if self.dataset_info(dataset)['namn'] == 'votering':
                yield self.base_url + dataset


