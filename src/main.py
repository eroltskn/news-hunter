from config import Config
from src.utils.app_helper import generate_new_uuid
from src.utils.file_helper import download_media_from_site, write_data_json_file
from src.utils.html_parser_helper import get_html_data_from_site, extract_paragraphs_from_html_data
from src.utils.rss_helper import get_rss_feed_result


def trigger_hunting():
    for category in Config.NEWS_CATEGORIES:
        print(category)
        rss_url = "{}/{}".format(Config.RSS_URL, category)
        feed = get_rss_feed_result(rss_url=rss_url)

        entry_list = feed.entries

        for entry in entry_list:
            html_data = get_html_data_from_site(entry)
            paragraphs = extract_paragraphs_from_html_data(html_data)

            filename = generate_new_uuid()
            write_data_json_file(category, entry, paragraphs, filename)

            download_media_from_site(entry["links"][1]["href"], filename)


if __name__ == "__main__":
    trigger_hunting()
