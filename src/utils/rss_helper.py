
import feedparser


def get_rss_feed_result(rss_url):
    return feedparser.parse(rss_url)