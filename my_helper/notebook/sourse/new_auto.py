from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import Qt
from my_helper.notebook.sourse.template import TempForm
designer_file = '../designer_ui/new_auto_2.ui'
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
        self.list_ui = [self.gov_number, self.model, self.brand, self.track_number]
        self.slice_set = len(self.list_ui)
        self.slice_get = len(self.list_ui) - 1
        self.slice_clean = len(self.list_ui)
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id

    def init_list(self):
        rows = self.parent.db.get_data("gov_number, model", self.table)
        self.cb_select.addItems(["(нет)"])
        if not rows:
            return False
        for row in rows:
            self.cb_select.addItems([" ".join((row[:2]))])

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))
        for item in self.list_ui[:4]:
            item.setValidator(symbols)

    def _ev_select(self, text):
        for row in self.rows_from_db:
            if text.split()[0] in row:
                self.set_data(row)
        return False

    def _get_data(self, data):
        data.append(self.track_number.text()) if self.is_track.isChecked() else data.append("")
        return data

    def _set_data(self, data):
        if self.track_number.text():
            self.is_track.setChecked(True)
        return True

    def _clean_data(self):
        return True

    def check_input(self):
        if "" in self.list_ui[:3]:
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


