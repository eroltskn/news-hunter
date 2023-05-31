import io
import os
import errno

import json
import urllib.request

from config import Config as CONFIG


def findout_difference_objects(old_record, new_record, category):
    result = False
    if old_record["detail"] != new_record["detail"]:
        old_record["detail"] = new_record["detail"]
        result = True

    if old_record["media"] != new_record["links"][1]["href"]:
        old_record["media"] = new_record["links"][1]["href"]
        download_media_from_site(link=new_record["links"][1]["href"],
                                 category=category,
                                 filename=old_record["filename"])
        result = True

    if old_record["title"] != new_record["title"]:
        old_record["title"] = new_record["title"]
        result = True

    if old_record["published"] != new_record["published"]:
        old_record["published"] = new_record["published"]
        result = True

    return result


def startup_check_for_json():
    for category in CONFIG.NEWS_CATEGORIES:
        path = "{}/{}.json".format(CONFIG.JSON_FILE_LOCATION, category)
        if os.path.isfile(path) and os.access(path, os.R_OK):
            # checks if file exists
            print("File exists and is readable")
        else:
            print("Either file is missing or is not readable, creating file...")
            with io.open(path, 'w') as news_file:
                news_file.write(json.dumps({}))


def startup_check_for_images():
    for category in CONFIG.NEWS_CATEGORIES:
        path = "{}/{}".format(CONFIG.IMAGE_FILE_LOCATION, category)
        try:
            os.makedirs(path)
        except OSError as e:
            if errno.EEXIST != e.errno:
                raise


def download_media_from_site(link, category, filename):
    urllib.request.urlretrieve(link,
                               "{}/{}/{}.jpg".format(CONFIG.IMAGE_FILE_LOCATION, category, filename))


def write_data_json_file(category, new_object, filename):
    dictionary = {
        "detail": new_object["detail"],
        "link": new_object["link"],
        "title": new_object["title"],
        "published": new_object["published"],
        "filename": filename,
        "media": new_object["links"][1]["href"]
    }

    with open("{}/{}.json".format(CONFIG.JSON_FILE_LOCATION, category), 'r+') as file:
        file_data = json.load(file)

        if "items" not in file_data:
            file_data["items"] = []

        for current_item in file_data["items"]:
            if current_item["link"] == new_object["link"]:

                if findout_difference_objects(old_record=current_item,
                                              new_record=new_object,
                                              category=category):
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                    file.truncate()
                else:
                    print("no difference for existing object")
                break
        else:
            file_data["items"].append(dictionary)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            download_media_from_site(link=new_object["links"][1]["href"],
                                     category=category,
                                     filename=filename)
