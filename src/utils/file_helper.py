import uuid
import json
import urllib.request

from config import Config as CONFIG


def write_data_json_file(category, single_object, paragraphs, filename):
    dictionary = {
        "id": single_object["id"],
        "detail": paragraphs,
        "link": single_object["link"],
        "published": single_object["published"],
        "filename": filename
    }

    json_object = json.dumps(dictionary, indent=4)

    with open("{}/{}.json".format(CONFIG.JSON_FILE_LOCATION, category), "w") as outfile:
        outfile.write(json_object)


def download_media_from_site(link, filename):
    urllib.request.urlretrieve(link,
                               "{}/{}.jpg".format(CONFIG.IMAGE_FILE_LOCATION, filename))
