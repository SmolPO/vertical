from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class BossPost(QDialog):
    def __init__(self, parent):
        super(BossPost, self).__init__()
        uic.loadUi('../designer_ui/boss_post.ui', self)
        # pass
        self.parent = parent
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.cb_family.addItems(["Щербаков", "Симаков"])
        self.cb_family.activated[str].connect(self.onActivated)

    def onActivated(self, text):
        self.family.setText(text)

    def ev_OK(self):
        # Проверить данные и отправка в БД
        new_post = list([self.family.text(), self.email.text()])
        self.parent.set_new_post(new_post)
        print("OK")
        self.close()

    def ev_cancel(self):
        print("cancel")
        self.close()
