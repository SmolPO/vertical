from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget

class NewBoss(QWidget):
    def __init__(self, main_window):
        super(NewBoss, self).__init__()
        uic.loadUi('../designer_ui/new_boss.ui', self)
        # pass
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.main_window = main_window

    def ev_OK(self):
        # Проверить данные и отправка в БД
        print("OK")
        self.close()

    def ev_cancel(self):
        print("cancel")
        self.close()
