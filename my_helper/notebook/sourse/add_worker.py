from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class AddWorker(QDialog):
    def __init__(self, parent=None):
        super(AddWorker, self).__init__(parent)
        uic.loadUi('../designer_ui/add_worker.ui', self)
        # pass
        self.parent = parent
        self.b_OK.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.worker = list()

    def ev_OK(self):
        # считать все данные из формы
        self.parent.get_new_worker(self.worker)
        print("OK")
        self.close()

    def ev_cancel(self):
        self.parent.get_new_worker(["not"])
        print("cancel")
        self.close()
