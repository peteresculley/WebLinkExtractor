import unittest
import queue
from consumer import Consumer


class ConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = queue.Queue(10)
        cls.consumer = Consumer(name='consumer', queue=cls.q)

    def test_create_file_name(self):
        file_name = Consumer.create_file_name(self.consumer, "http://www.netflix.com")
        self.assertEqual(file_name, "netflix.com")
        file_name = Consumer.create_file_name(self.consumer, "http://www.python.org/doc/")
        self.assertEqual(file_name, "python.org")

    def test_parse_links_from_html(self):
        file = open("netflix.com.html", "r")
        html_1 = file.read()
        file.close()
        html_2 = ""
        result_1 = Consumer.parse_links_from_html(self.consumer, html_1)
        self.assertEqual(len(result_1), 1, "Equal lengths in first example")
        self.assertEqual(result_1[0].get("href"), "http://ir.netflix.com/", "Equal contents in first example")
        result_2 = Consumer.parse_links_from_html(self.consumer, html_2)
        self.assertEqual(len(result_2), 0, "Equal lengths in second example")
        self.assertEqual(result_2, [], "Equal contents in second example")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ConsumerTests("test_create_file_name"))
    suite.addTest(ConsumerTests("test_parse_links_from_html"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
