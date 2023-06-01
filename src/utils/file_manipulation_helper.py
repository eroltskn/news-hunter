import os

import json
import urllib.request

from src.config import Config as CONFIG
from src.utils.app_helper import get_datetime_iso_format


def find_out_difference_objects(old_record, new_record, category):
    result = False
    if old_record["detail"] != new_record["detail"]:
        old_record["detail"] = new_record["detail"]
        result = True

    if old_record["media"] != new_record["links"][1]["href"]:
        old_record["media"] = new_record["links"][1]["href"]

        remove_file_from(category=category,
                         filename=old_record["filename"])

        download_media_from_site(link=new_record["links"][1]["href"],
                                 category=category,
                                 filename=old_record["filename"])
        result = True

    if old_record["title"] != new_record["title"]:
        old_record["title"] = new_record["title"]
        result = True

    new_datetime_formatted = get_datetime_iso_format(new_record["published"])
    if old_record["published"] != new_datetime_formatted:
        old_record["updated"] = new_datetime_formatted
        result = True

    if old_record["link"] != new_record["link"]:
        old_record["link"] = new_record["link"]
        result = True

    return result


def download_media_from_site(link, category, filename):
    urllib.request.urlretrieve(link,
                               "{}/{}/{}.jpg".format(CONFIG.IMAGE_FILE_LOCATION, category, filename))


def remove_file_from(category, filename):
    removed_file = "{}/{}/{}".format(CONFIG.IMAGE_FILE_LOCATION,
                                     category,
                                     filename)
    if os.path.isfile(removed_file):
        os.unlink(removed_file)


def write_data_json_file(category, new_object, filename):
    dictionary = {
        "id": new_object["id"],
        "detail": new_object["detail"],
        "link": new_object["link"],
        "title": new_object["title"],
        "published": get_datetime_iso_format(new_object["published"]),
        "filename": filename,
        "media": new_object["links"][1]["href"]
    }

    with open("{}/{}.json".format(CONFIG.JSON_FILE_LOCATION, category), 'r+') as file:
        file_data = json.load(file)

        if "items" not in file_data:
            file_data["items"] = []

        for current_item in file_data["items"]:
            if current_item["id"] == new_object["id"]:
                is_found = find_out_difference_objects(old_record=current_item,
                                                       new_record=new_object,
                                                       category=category)
                if is_found:
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                    file.truncate()

                break
        else:
            file_data["items"].append(dictionary)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            download_media_from_site(link=new_object["links"][1]["href"],
                                     category=category,
                                     filename=filename)
