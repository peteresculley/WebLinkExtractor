import threading
import time
import logging
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-8s) %(message)s', )
logging.basicConfig(level=logging.ERROR,
                    format='(%(threadName)-8s) %(message)s', )


class Consumer(threading.Thread):
    def __init__(self, target=None, name=None, queue=None):
        super(Consumer, self).__init__()
        self.target = target
        self.name = name
        self.queue = queue

    def run(self):
        while True:
            if self.queue is not None:
                if not self.queue.empty():
                    queue_item = self.queue.get()
                    url = queue_item["url"];
                    file_name = self.create_file_name(url)
                    links_file = self.open_output_file(file_name)
                    if links_file is not None:
                        links = self.parse_links_from_html(queue_item["url_html"])
                        for link in links:
                            links_file.write(link.get("href") + "\n")
                        logging.debug(str(len(links)) + " links found on " + str(url)
                                      + " and written to file: " + str(links_file.name))
                        logging.debug(str(self.queue.qsize()) + ' more items in queue')
                        links_file.close()
                else:
                    self.wait_with_message("Queue empty.", 5)
            else:
                self.wait_with_message("No queue yet.", 5)
        return

    def assign_queue(self, queue):
        self.queue = queue

    def create_file_name(self, url):
        file_name = url[url.find("www") + 4:]
        slash_position = file_name.find("/")
        if slash_position > -1:
            file_name = file_name[:slash_position]
        return file_name

    def open_output_file(self, file_name):
        full_file_name = "links/" + file_name + ".%d.txt" % time.time()
        output_file = None
        try:
            output_file = open(full_file_name, "w")
        except OSError:
            logging.error("Cannot open file " + full_file_name + " for writing")
        return output_file

    def parse_links_from_html(self, html):
        soup = BeautifulSoup(html, "html5lib")
        return soup.findAll('a', attrs={'href': re.compile("^http://")})

    def wait_with_message(self, message, seconds):
        logging.debug(message + " Waiting " + str(seconds) + " seconds...")
        time.sleep(seconds)
