import unittest
from .. import translation
from .. import gtfs

class Translation_Tests(unittest.TestCase):
    def test_group_by_invalid_field(self):
        stops = [gtfs.Stop("1"), gtfs.Stop("2")]
        result = translation.group_by("invalid", stops)
        self.assertEqual(len(result.items()), 0)

    def test_group_by_valid_field(self):
        stops = [gtfs.Stop("1"), gtfs.Stop("2"), gtfs.Stop("1")]
        result = translation.group_by("stop_id", stops)
        self.assertEqual(len(result.items()), 2)
        self.assertEqual(len(result["1"]), 2)


if __name__ == "__main__":
    unittest.main()