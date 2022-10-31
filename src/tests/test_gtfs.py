import csv
import unittest
from .. import gtfs
from unittest.mock import Mock, patch, mock_open


class GTFS_Tests(unittest.TestCase):
    def test_load_gtfs_from_file_none_filename(self):
        with self.assertRaises(ValueError):
            gtfs.load_gtfs_from_file(None, gtfs.Stop)

    def test_load_gtfs_from_file_empty_filename(self):
        with self.assertRaises(ValueError):
            gtfs.load_gtfs_from_file("", gtfs.Stop)
    
    def test_load_gtfs_from_file_none_obj(self):
        with self.assertRaises(ValueError):
            gtfs.load_gtfs_from_file("valid", None)

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_load_gtfs_from_file_csv_error(self, open_mock):
        csv.DictReader = Mock(side_effect=Exception("TEST"))
        with self.assertRaises(Exception, msg="Should encounter exception"):
            gtfs.load_gtfs_from_file("valid", gtfs.Stop)


if __name__ == "__main__":
    unittest.main()