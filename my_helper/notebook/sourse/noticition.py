import threading


class QueueNotic(threading.Thread):
    def __init__(self, queue):
        self.queue = queue
        pass

    def run(self):
        while True:
            pass
        pass