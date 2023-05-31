from config import Config
from src.utils.app_helper import generate_new_uuid
from src.utils.file_helper import download_media_from_site, \
    write_data_json_file,  startup_check_for_images, startup_check_for_json
from src.utils.html_parser_helper import get_html_data_from_site, \
    extract_paragraphs_from_html_data
from src.utils.rss_helper import get_rss_feed_result


def trigger_hunting():
    for category in Config.NEWS_CATEGORIES:
        print(category)
        rss_url = "{}/{}".format(Config.RSS_URL, category)
        feed = get_rss_feed_result(rss_url=rss_url)

        entry_list = feed.entries

        for new_object in entry_list:
            html_data = get_html_data_from_site(new_object=new_object)
            paragraphs = extract_paragraphs_from_html_data(html_data=html_data)

            new_object["detail"] = paragraphs
            filename = generate_new_uuid()
            write_data_json_file(category=category, new_object=new_object, filename=filename)


if __name__ == "__main__":
    startup_check_for_json()
    startup_check_for_images()
    trigger_hunting()
