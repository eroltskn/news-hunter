import unittest
from bs4 import BeautifulSoup

from src.utils.html_parser_helper import extract_paragraphs_from_html_data, get_html_data_from_site


class TestOne(unittest.TestCase):
    def setUp(self):
        self.html_data_raw = '''
            <html class="no-js" lang="tr">
                             <div class="_3QVZl" style="font-size:16px">
                                <div>
                                    <html>
                                        <head></head>
                                        <body>
                                            <p>first paragraph.</p>      
                                            <p>second paragraph.</p>
                                            <p>third paragraph.</p>
                                        </body>
                                    </html>
                                </div>
                             </div>
            </html>
        '''

        self.link = "https://www.google.com/"
        self.link2 = "https://www.google_erol.com/"

    def test_extract_html_data(self):
        html_data = BeautifulSoup(self.html_data_raw, "html.parser")

        paragraphs = extract_paragraphs_from_html_data(html_data)

        self.assertIn("first paragraph", paragraphs, msg=str(html_data))
        self.assertIn("second paragraph", paragraphs, msg=str(html_data))
        self.assertIn("third paragraph", paragraphs, msg=str(html_data))

        self.assertNotIn("fourth paragraph", paragraphs, msg=str(html_data))

    def test_getting_html_data(self):
        html_data = get_html_data_from_site(link=self.link)

        self.assertGreater(len(html_data), 0)

        html_data = get_html_data_from_site(link=self.link2)

        self.assertEqual(html_data, None)


if __name__ == '__main__':
    unittest.main()
