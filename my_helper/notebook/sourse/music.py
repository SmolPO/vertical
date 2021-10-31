from PyQt5.QtWidgets import  QMessageBox
import webbrowser
from my_helper.notebook.sourse.create.new_template import TempForm
from database import get_path_ui
import logging
# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("web")


class Web(TempForm):
    def __init__(self, parent=None):
        super(Web, self).__init__(designer_file)
        self.parent = parent
        self.table = "musics"
        self.b_start.clicked.connect(self.ev_start)
        self.parent.db.init_list(self.cb_select, "name", self.table)
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.list_ui = [self.name, self.add_link]
        self.slice_set = len(self.list_ui)
        self.slice_get = len(self.list_ui)
        self.slice_clean = len(self.list_ui)
        self.slice_select = -1
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id

    def ev_start(self):
        for row in self.parent.db.get_data("name, link", self.table):
            if self.cb_select.currentText() in row:
                webbrowser.open(row[1])
        self.close()

    def check_input(self):
        data = list((self.name.text(), self.add_link.text()))
        if "" in data:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return False
        return True

    def _clean_data(self):
        return True

    def _ev_select(self, text):
        self.slice_select = len(text)
        return True

    def _set_data(self, data):
        return True

    def _get_data(self, data):
        return data

    def _but_status(self, status):
        return True

    def _ev_ok(self):
        return True
