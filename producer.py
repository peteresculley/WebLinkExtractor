import threading
import time
import logging
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-8s) %(message)s', )
logging.basicConfig(level=logging.ERROR,
                    format='(%(threadName)-8s) %(message)s', )


class Producer(threading.Thread):
    def __init__(self, target=None, name=None, queue=None, urls_files=None):
        super(Producer, self).__init__()
        self.target = target
        self.name = name
        self.queue = queue
        if urls_files is not None:
            self.urls_files = urls_files
        else:
            self.urls_files = []

    def run(self):
        urls = []
        while True:
            if self.queue is not None:
                if not self.queue.full():
                    if len(self.urls_files) > 0:
                        while len(self.urls_files) > 0:
                            urls_file = self.urls_files.pop()
                            urls.extend(self.read_urls_from_file(urls_file))

                            while len(urls) > 0:
                                url = urls.pop()
                                queue_item = self.read_html_from_url(url)
                                self.queue.put(queue_item)
                                logging.debug(str(self.queue.qsize()) + ' items in queue after adding data for ' + str(url))
                    else:
                        self.wait_with_message("No new files for processing.", 5)
                else:
                    # self.wait_with_message("Full queue.", 5)
                    self.remove_oldest_elements_from_queue(5)
            else:
                self.wait_with_message("No queue yet.", 5)
        return

    def assign_queue(self, queue):
        self.queue = queue

    def read_urls_from_file(self, file_name):
        urls = []
        try:
            f = open(file_name, "r")
            urls = f.readlines()  # test with empty file
            urls = [x.strip() for x in urls]
            f.close()
        except OSError:
            logging.error("Cannot open file " + file_name)
            logging.error(OSError.args)
        except Exception:
            logging.error("Error happened while reading file " + file_name)
            f.close()

        return urls

    def read_html_from_url(self, url):
        url_html = ""
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            fp = urlopen(req)
            url_bytes = fp.read()
            url_html = url_bytes.decode("utf8")
            fp.close()
        except Exception:
            logging.error("Exception happened while trying to read from url " + url)

        return {"url": url, "url_html": url_html}

    def add_file(self, file_name):
        self.urls_files.append(file_name)

    def wait_with_message(self, message, seconds):
        logging.debug(message + " Waiting " + str(seconds) + " seconds...")
        time.sleep(seconds)

    def remove_oldest_elements_from_queue(self, count):
        for i in range(0,count):
            if not self.queue.empty():
                self.queue.get()
            else:
                break
