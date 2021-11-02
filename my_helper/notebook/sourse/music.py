from PyQt5.QtWidgets import  QMessageBox
import webbrowser
from my_helper.notebook.sourse.create.new_template import TempForm
from database import get_path_ui, my_errors
from PyQt5.QtWidgets import QMessageBox as mes
import logging
# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("web")


class Web(TempForm):
    def __init__(self, parent=None):
        super(Web, self).__init__(designer_file, parent, "links")
        if not self.status_:
            return
        self.b_start.clicked.connect(self.ev_start)
        self.parent.db.init_list(self.cb_select, "name", self.table)
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.list_ui = [self.name, self.add_link]
        self.slice_set = len(self.list_ui)
        self.slice_get = len(self.list_ui)
        self.slice_clean = len(self.list_ui)
        self.slice_select = -1
        self.current_id = self.next_id

    def ev_start(self):
        try:
            rows = self.parent.db.get_data("name, link", self.table)
        except:
            mes.question(self, "Сообщение", my_errors["11_kill"], mes.Cancel)
            return
        for row in rows:
            if self.cb_select.currentText() in row:
                try:
                    webbrowser.open(row[1])
                except:
                    mes.question(self, "Сообщение", my_errors["12_web"] + row[1], mes.Cancel)
                    return
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
