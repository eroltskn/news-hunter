import unittest

from src.utils.app_helper import get_datetime_iso_format, \
    generate_new_uuid


class FileManipulation(unittest.TestCase):

    def setUp(self):
        pass

    def test_uuid_generation(self):
        uuid = generate_new_uuid()

        self.assertGreater(len(uuid), 0)

    def test_iso_format(self):
        raw_datetime = "Fri, 02 Jun 2023 08:01:05 GMT"
        datetime_formatted = get_datetime_iso_format(raw_datetime)

        self.assertEqual(datetime_formatted, "2023-06-02T08:01:05+00:00")


if __name__ == '__main__':
    unittest.main()
