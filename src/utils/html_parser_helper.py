import requests
from bs4 import BeautifulSoup

from src.config import Config as CONFIG


def get_html_data_from_site(link):
    html_data = None
    try:
        url = link
        page = requests.get(url)
        html_data = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        print(str(e))

    return html_data


def extract_paragraphs_from_html_data(html_data):
    concat_paragraphs = []
    try:
        div_element = html_data.find_all("div", class_=CONFIG.HTML_CLASS_NAME)

        paragraphs = div_element[0].find_all("p")

        concat_paragraphs = "".join([para.text for para in paragraphs])
    except Exception as e:
        print(str(e))

    return concat_paragraphs
