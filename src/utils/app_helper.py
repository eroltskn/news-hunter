import os
import io
import errno

import json
import uuid
import dateutil.parser as parser

from src.config import Config as CONFIG


def generate_new_uuid():
    return str(uuid.uuid4())


def get_datetime_iso_format(datetime_str):
    date = parser.parse(datetime_str)
    return date.isoformat()


def create_json_file_startup():
    for category in CONFIG.NEWS_CATEGORIES:
        path = "{}/{}.json".format(CONFIG.JSON_FILE_LOCATION, category)
        if os.path.isfile(path) and os.access(path, os.R_OK):
            # checks if file exists
            print("File exists and is readable")
        else:
            print("Either file is missing or is not readable, creating file...")
            with io.open(path, 'w') as news_file:
                news_file.write(json.dumps({}))


def create_folders_startup():
    try:
        for category in CONFIG.NEWS_CATEGORIES:
            path = "{}/{}".format(CONFIG.IMAGE_FILE_LOCATION, category)
            os.makedirs(path)

        os.makedirs(CONFIG.JSON_FILE_LOCATION)
    except OSError as e:
        if errno.EEXIST != e.errno:
            raise
