from config import Config as CONFIG
from src.utils.app_helper import generate_new_uuid
from src.utils.file_manipulation_helper import write_data_json_file,  create_folders_startup, \
    create_json_file_startup
from src.utils.html_parser_helper import get_html_data_from_site, \
    extract_paragraphs_from_html_data
from src.utils.rss_helper import get_rss_feed_result


def trigger_hunting():
    for category in CONFIG.NEWS_CATEGORIES:
        print(category)
        rss_url = "{}/{}".format(CONFIG.RSS_URL, category)
        feed = get_rss_feed_result(rss_url=rss_url)

        entry_list = feed.entries

        for new_object in entry_list:
            print(new_object.keys())
            html_data = get_html_data_from_site(new_object=new_object)
            paragraphs = extract_paragraphs_from_html_data(html_data=html_data)

            new_object["detail"] = paragraphs
            filename = generate_new_uuid()
            write_data_json_file(category=category, new_object=new_object, filename=filename)


if __name__ == "__main__":
    create_folders_startup()
    create_json_file_startup()
    trigger_hunting()
