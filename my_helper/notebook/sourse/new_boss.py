from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class NewBoss(QDialog):
    def __init__(self, parent):
        super(NewBoss, self).__init__()
        uic.loadUi('../designer_ui/new_boss.ui', self)
        # pass
        self.parent = parent
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)

    def ev_OK(self):
        # Проверить данные и отправка в БД
        new_boss = list([self.post.text(), self.name.text()])
        self.parent.set_new_boss(new_boss)
        print("OK")
        self.close()

    def ev_cancel(self):
        print("cancel")
        self.close()
