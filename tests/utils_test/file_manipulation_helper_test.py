import json
import unittest
import copy

from src.utils.app_helper import create_folders_startup, create_json_file_startup, get_datetime_iso_format
from src.utils.file_manipulation_helper import find_out_difference_objects, write_data_json_file
from src.config import Config as CONFIG


class FileManipulation(unittest.TestCase):

    def setUp(self):
        self.old_record1 = {
            "id": "https://www.google.com/",
            "detail": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt"
                      " ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation"
                      " ullamco laboris nisi ut aliquip ex ea commodo consequat",
            "link": "https://www.google.com/",
            "title": "Lorem ipsum dolor sit amet",
            "published": "2023-06-02T07:30:05+00:00",
            "filename": "98881967-544f-4f42-91b9-f9fed0f1469e",
            "media": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        }

        self.new_record1 = {
            "id": "https://www.google.com/",
            "detail": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
            "link": "https://www.google.com/",
            "title": "Lorem ipsum dolor sit amet",
            "published": "Fri, 02 Jun 2023 07:30:05 ",
            "filename": "98881967-544f-4f42-91b9-f9fed0f1469e.jpg",
            'links': [{'rel': 'alternate', 'type': 'text/html',
                       'href': 'https://www.google.com/'},
                      {'length': '0', 'type': 'image/png',
                       'href': 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png',
                       'rel': 'enclosure'}],

        }

        self.new_record2 = {
            "id": "https://www.google.com/",
            "detail": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
            "link": "https://www.google.com/",
            "title": "Lorem ipsum dolor sit amet update",
            "published": "Fri, 02 Jun 2023 22:30:05 ",
            "filename": "98881967-544f-4f42-91b9-f9fed0f1469e.jpg",
            'links': [{'rel': 'alternate', 'type': 'text/html',
                       'href': 'https://www.google.com/'},
                      {'length': '0', 'type': 'image/png',
                       'href': 'https://t24.com.tr/assets/96718156.png',
                       'rel': 'enclosure'}],

        }

        create_folders_startup()
        create_json_file_startup()

    def test_finding_out_difference(self):
        old_record_copy = copy.deepcopy(self.old_record1)
        find_out_difference_objects(old_record=self.old_record1, new_record=self.new_record1, category="gundem")
        self.assertNotEqual(old_record_copy["detail"], self.old_record1["detail"])
        self.assertEqual(old_record_copy["published"], self.old_record1["published"])
        self.assertEqual(old_record_copy["link"], self.old_record1["link"])

    def test_writing_json_file(self):
        category = "gundem"
        write_data_json_file(category=category, new_object=self.new_record1)

        with open("{}/{}.json".format(CONFIG.JSON_FILE_LOCATION, category), 'r') as file:
            file_data = json.load(file)

            recently_added = file_data["items"][0]

            self.assertEqual(self.new_record1["link"], recently_added["link"])
            self.assertEqual(self.new_record1["filename"], recently_added["filename"])
            self.assertEqual(self.new_record1["title"], recently_added["title"])

        write_data_json_file(category=category, new_object=self.new_record2)

        with open("{}/{}.json".format(CONFIG.JSON_FILE_LOCATION, category), 'r') as file:
            file_data = json.load(file)

            recently_added = file_data["items"][0]

            self.assertEqual(self.new_record2["links"][1]["href"], recently_added["media"])
            self.assertNotEqual(self.new_record2["links"][1]["href"], self.new_record1["links"][1]["href"])
            self.assertEqual(self.new_record2["filename"], recently_added["filename"])
            self.assertNotEqual(get_datetime_iso_format(self.new_record2["published"]), recently_added["published"])


if __name__ == '__main__':
    unittest.main()
