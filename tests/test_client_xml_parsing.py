# Standard library imports...
from unittest.mock import Mock, patch

# Third-party imports...
from nose.tools import assert_is_not_none, assert_equal, assert_true

# Local imports...
from dataset_metadata import xml_metadata
from RiksdagenDataDownloader.riksdagen_client import RiksdagenClient

class TestClient(object):
    @classmethod
    def setup_class(cls):
        fake_xml = xml_metadata(5, 'xml', 'ip')
        mock_response = Mock()
        mock_response.return_value.content = fake_xml

        cls.mock_get_patcher = patch('RiksdagenDataDownloader.riksdagen_client.requests.get', side_effect=mock_response)
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_documents_not_empty_after_instansiation(self):
        riks_client = RiksdagenClient()
        assert_is_not_none(riks_client.documents) 

    def test_expected_format_is_available(self):
        riks_client = RiksdagenClient()
        available_formats = riks_client.available_formats()
        assert_true('xml' in available_formats)

    def test_expected_collection_is_available(self):
        riks_client = RiksdagenClient()
        available_collections = riks_client.available_collections()
        assert_true('ip' in available_collections)