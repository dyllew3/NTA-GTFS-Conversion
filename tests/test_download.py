import unittest
from unittest.mock import Mock, patch, mock_open
from src import download
from . import utils
import os
DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def load_zip_bytes(filename):
    with open(filename, 'rb') as open_file:
        result = open_file.read()
        return result
class Download_Tests(unittest.TestCase):
    def test_constructor(self):
        download.DownloadService()
    
    @patch('requests.get', side_effect=lambda *args,  **newkeywargs: utils.MockResponse(None, 404))
    def test_request_error(self, mock_get):
        with self.assertRaises(Exception):
            service = download.DownloadService()
            service.get_if_diff("something")

    @patch('requests.get', side_effect=lambda *args,  **newkeywargs: utils.MockResponse(load_zip_bytes(os.path.join(DIRECTORY, "resources","valid.zip")), 200))
    def test_get_zip(self, mock_get):
        service = download.DownloadService()
        filezip = service.get_if_diff("something")
        self.assertEqual(filezip.filename, None, "Filename be none")
        self.assertIn("trips.txt",[ x.filename for x in filezip.filelist])

    @patch('requests.get', side_effect=lambda *args,  **newkeywargs: utils.MockResponse(load_zip_bytes(os.path.join(DIRECTORY, "resources", "valid.zip")), 200))
    def test_get_zip_no_diff(self, mock_get):
        service = download.DownloadService()
        filezip = service.get_if_diff("something")
        self.assertEqual(filezip.filename, None, "Filename be none")
        self.assertIn("trips.txt",[ x.filename for x in filezip.filelist])
        
        filezip = service.get_if_diff("something")
        self.assertEqual(filezip, None, "Second call should be none as content should be saved")


if __name__ == "__main__":
    unittest.main()