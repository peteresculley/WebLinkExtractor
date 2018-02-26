import queue
from producer import Producer
from consumer import Consumer
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )
BUF_SIZE = 20
q = queue.Queue(BUF_SIZE)

if __name__ == '__main__':
    producer = Producer(name='producer')
    consumer = Consumer(name='consumer')

    producer.start()
    consumer.start()

    producer.assign_queue(q)
    consumer.assign_queue(q)

    producer.add_file("urls/urls.txt")
    time.sleep(60)
    producer.add_file("urls/urls1.txt")
