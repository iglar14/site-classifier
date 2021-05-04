import unittest

from req import strip_url_beginning, get_main_page_url, specify_scheme


class TestUrls(unittest.TestCase):
    def test_strip_beginning(self):
        self.assertEqual(strip_url_beginning('www.microsoft.com'), 'microsoft.com')
        self.assertEqual(strip_url_beginning('https://www.microsoft.com'), 'microsoft.com')
        self.assertEqual(strip_url_beginning('http://www.microsoft.com'), 'microsoft.com')
        self.assertEqual(strip_url_beginning('microsoft.com'), 'microsoft.com')
        self.assertEqual(strip_url_beginning('https://microsoft.com'), 'microsoft.com')
        self.assertEqual(strip_url_beginning('http://microsoft.com'), 'microsoft.com')

    def test_get_main_page(self):
        self.assertEqual(get_main_page_url('microsoft.com'), 'microsoft.com')
        self.assertEqual(get_main_page_url('http://www.microsoft.com/'), 'http://www.microsoft.com')
        self.assertEqual(get_main_page_url('http://www.microsoft.com/1/s/index.html'), 'http://www.microsoft.com')
        self.assertEqual(get_main_page_url('microsoft.com/1/s/index.html'), 'microsoft.com')
        self.assertEqual(get_main_page_url('www.microsoft.com/1/s/index.html'), 'www.microsoft.com')

    def test_specify_scheme_adds_scheme(self):
        self.assertEqual(specify_scheme('microsoft.com'), 'http://microsoft.com')
        self.assertEqual(specify_scheme('microsoft.com', 'https://'), 'https://microsoft.com')

    def test_specify_scheme_leaves_existing_scheme_unchanged(self):
        self.assertEqual(specify_scheme('ftp://microsoft.com', 'https://'), 'ftp://microsoft.com')

if __name__ == '__main__':
    unittest.main()
