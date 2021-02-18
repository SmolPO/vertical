from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class ChosePeople(QDialog):
    def __init__(self, rows):
        super(ChosePeople, self).__init__()
        uic.loadUi('../designer_ui/chose_people.ui', self)
        # pass
        self.b_OK.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.rows = rows

    def ev_OK(self):
        print("OK")

    def ev_cancel(self):
        print("cancel")
