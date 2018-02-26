import unittest
import queue
from producer import Producer


class ProducerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = queue.Queue(10)
        cls.producer = Producer(name='producer', queue=cls.q)

    def test_read_urls_from_file(self):
        urls = Producer.read_urls_from_file(self.producer, "urls/urls.txt")
        self.assertEqual(len(urls), 2, "Equal sizes")
        self.assertEqual(urls, ["http://www.python.org/doc/", "http://www.netflix.com"], "Equal content")
        urls = Producer.read_urls_from_file(self.producer, "urls/empty_urls.txt")
        self.assertEqual(len(urls), 0, "Equal sizes for empty file")
        self.assertEqual(urls, [], "Equal content for empty file")

    def test_read_html_from_url(self):
        html = Producer.read_html_from_url(self.producer, "http://www.python.org")
        self.assertEqual(html["url_html"][0:15], "<!doctype html>", "Equal start")
        self.assertEqual(str(html["url_html"][len(html["url_html"]) - 8:]).strip(), "</html>", "Equal end")

    def test_add_file(self):
        self.assertEqual(len(self.producer.urls_files), 0, "No files")
        Producer.add_file(self.producer, "urls/urls.txt")
        self.assertEqual(len(self.producer.urls_files), 1, "One file added")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ProducerTests("test_read_urls_from_file"))
    suite.addTest(ProducerTests("test_read_html_from_url"))
    suite.addTest(ProducerTests("test_add_file"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
