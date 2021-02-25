from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class NewContact(QDialog):
    def __init__(self, parent=None):
        super(NewContact, self).__init__(parent)
        uic.loadUi('../designer_ui/new_contract.ui', self)
        # pass
        self.parent = parent
        self.b_OK.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.worker = list()

    def ev_OK(self):
        # считать все данные из формы
        print("OK")
        self.close()

    def ev_cancel(self):
        print("cancel")
        self.close()
