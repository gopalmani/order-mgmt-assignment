import threading
import queue
from models import update_order_status

class QueueManager:
    def __init__(self, num_workers=4):
        self.queue = queue.Queue()
        self.num_workers = num_workers
        self.workers = []

    def start(self):
        for _ in range(self.num_workers):
            worker = threading.Thread(target=self.process, daemon=True)
            worker.start()
            self.workers.append(worker)

    def process(self):
        while True:
            order_id = self.queue.get()
            try:
                update_order_status(order_id, 'processing')
                # We can add actual order processing logic here - payment validation, inventory checks, fraud checks. 
                update_order_status(order_id, 'completed')
            finally:
                self.queue.task_done()

    def add_order(self, order_id):
        self.queue.put(order_id)