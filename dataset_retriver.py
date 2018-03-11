import requests
import xmltodict

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
        
        # Get the XML file
        self.data_xml = requests.get(xml_url)

        # Make sure we sure we got an OK
        if self.data_xml.status_code == 200:
            # Change bytes to UTF-8 string
            self.clean_xml = ''.join([line.decode('utf-8') for line in self.data_xml.iter_lines()])
            # Parse to a xml dict structure
            self.xml_dict = xmltodict.parse(self.clean_xml)
        else:
            print("Something went wrong when retriving the dataset, make \
            sure the URL is correct.")

    def available_formats(self):
        """ Returns a list of all the available data formats """
        formats = []
        for dataset in self.xml_dict['datasetlista']['dataset']:
            if dataset['format'] not in formats:
                formats.append(dataset['format'])
        return formats

    def get_all_dataset_uri(self, data_type='sql'):
        """ Yield all the URIs to all the available datasets of that type. """
        for dataset in self.xml_dict['datasetlista']['dataset']:
            if dataset['format'] == data_type:
                yield self.base_url + dataset['url']
        
    def get_all_dataset_uri_size(self, data_type='sql'):
        """ Yield all the URIs to all the available datasets of that type
        and the size of the dataset as a tuple. """
        for dataset in self.xml_dict['datasetlista']['dataset']:
            if dataset['format'] == data_type:
                yield (self.base_url + dataset['url'], dataset['storlek'])
                
    def get_all_anforande_uri(self, data_type='sql'):
        """ Yield all the URIs for document type anforande. """
        for dataset in self.xml_dict['datasetlista']['dataset']:
            if dataset['format'] == data_type and dataset['namn'] == 'anforande':
                yield self.base_url + dataset['url']

    def get_all_dokument_uri(self, data_type='sql'):
        """ Yield all the URIs for document type dokument. """
        for dataset in self.xml_dict['datasetlista']['dataset']:
            if dataset['format'] == data_type and dataset['namn'] == 'dokument':
                yield self.base_url + dataset['url']

    def get_all_dokument_uri(self, data_type='sql'):
        """ Yield all the URIs for document type dokument. """
        for dataset in self.xml_dict['datasetlista']['dataset']:
            if dataset['format'] == data_type and dataset['namn'] == 'dokument':
                yield self.base_url + dataset['url']

    def get_all_person_uri(self, data_type='sql'):
        """ Yield all the URIs for document type person. """
        for dataset in self.xml_dict['datasetlista']['dataset']:
            if dataset['format'] == data_type and dataset['namn'] == 'person':
                yield self.base_url + dataset['url']

    def get_all_votering_uri(self, data_type='sql'):
        """ Yield all the URIs for document type votering. """
        for dataset in self.xml_dict['datasetlista']['dataset']:
            if dataset['format'] == data_type and dataset['namn'] == 'votering':
                yield self.base_url + dataset['url']
