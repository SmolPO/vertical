from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import Qt
from my_helper.notebook.sourse.create.new_template import TempForm
from my_helper.notebook.sourse.database import get_path_ui

#  logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("new_auto")
fields = ["model", "brand", "gov_number", "track_number", "id"]


class NewAuto(TempForm):
    def __init__(self, parent=None):
        super(NewAuto, self).__init__(designer_file)
        self.parent = parent
        self.table = "auto"
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.is_track.stateChanged.connect(self.have_track)
        self.init_list()
        self.track_number.setEnabled(False)
        self.list_ui = [self.gov_number, self.brand, self.model,  self.track_number]
        self.slice_set = len(self.list_ui)
        self.slice_get = len(self.list_ui) - 1
        self.slice_clean = len(self.list_ui)
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id
        self.track_number.setText("(нет)")

    def init_list(self):
        rows = self.parent.db.get_data("id, gov_number, model", self.table)
        self.cb_select.addItems(["(нет)"])
        if not rows:
            return False
        for row in rows:
            self.cb_select.addItems([row[0] + ". " + row[1] + " " + row[2]])

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))
        for item in self.list_ui[:4]:
            item.setValidator(symbols)

    def _get_data(self, data):
        data.append(self.track_number.text()) if self.is_track.isChecked() else data.append("(нет)")
        return data

    def _set_data(self, data):
        if not self.track_number.text() or self.track_number.text() == "(нет)":
            self.is_track.setChecked(False)
        else:
            self.is_track.setChecked(True)
        return True

    def check_input(self):
        data = self.get_data()
        if "" in data:
            mes.question(self, "Сообщение", "Заполните все поля", mes.Cancel)
            return False
        if self.is_track.isChecked() and self.track_number.text() == "":
            mes.question(self, "Внимание", "Так есть прицеп или нет??.. Введите номер или уберите галочку", mes.Cancel)
            return False
        return True

    def have_track(self, state):
        if state == Qt.Checked:
            self.track_number.setEnabled(True)
        else:
            self.track_number.setEnabled(False)
            self.track_number.setText("(нет)")

    def _clean_data(self):
        self.is_track.setChecked(False)
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True

    def _ev_select(self, text):
        return True