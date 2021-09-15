from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
import webbrowser
from my_helper.notebook.sourse.inserts import get_from_db, update_mat
designer_file = '../designer_ui/music.ui'


class Music(QDialog):
    def __init__(self, parent=None):
        super(Music, self).__init__(parent)
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.bosses = []
        self.table = "music"

        self.b_ok.clicked.connect(self.ev_start)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_add.clicked.connect(self.ev_add)
        self.b_change.clicked.connect(self.ev_change)
        self.b_kill.clicked.connect(self.ev_kill)
        self.cb_music.activated[str].connect(self.ev_select)

        for row in self.from_db("name", self.table):
            self.cb_music.addItems([row[0]])

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()

    def ev_add(self):
        data = self.get_data()
        if not data:
            return
        self.parent.get_new_data(data)
        self.close()

    def ev_start(self):
        for row in self.from_db("name, link", self.table):
            if self.cb_music.currentText() in row:
                webbrowser.open(row[1])
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_change(self):
        for row in self.from_db("name", self.table):
            if self.name.text() in row:
                self.my_update()

    def ev_kill(self):
        for row in self.from_db("name", self.table):
            if self.name.text() in row:
                data = [self.name.text(),  self.add_link.text()]
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.db.execute("DELETE FROM {0} WHERE name = '{1}'".format(
                        self.table, self.name.text()))
                    self.parent.db_conn.commit()
                    self.close()
                    return
                if answer == QMessageBox.Cancel:
                    return

    def set_data(self, data):
        self.name.setText(data[0])
        self.add_link.setText(data[1])

    def get_data(self):
        data = list((self.name.text(), self.add_link.text()))
        if "" in data:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return False
        return data

    def clean_data(self):
        self.name.setText("")
        self.add_link.setText("")

    def my_update(self):
        self.ev_kill()
        self.parent.get_new_data(self.get_data())
        self.close()

    def ev_select(self):
        for row in self.from_db("name, link", self.table):
            if self.cb_music.currentText() in row:
                self.set_data(row)

