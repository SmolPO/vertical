from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.template import TempForm
designer_file = '../designer_ui/new_worker.ui'


class NewWorker(TempForm):
    def __init__(self, parent=None):
        super(NewWorker, self).__init__(designer_file)
        # pass
        self.parent = parent
        self.table = "workers"
        self.init_mask()
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)
        self.parent.db.init_list(self.cb_contract, "name", "contracts")
        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = len(self.list_ui)
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я ]{30}"))
        number_prot = QREVal(QRE("[А-Яа-я _/- 0-9]{10}"))

        self.family.setValidator(symbols)
        self.name.setValidator(symbols)
        self.surname.setValidator(symbols)
        self.post.setValidator(symbols)
        self.phone.setValidator(QREVal(QRE("[0-9]{11}")))
        self.passport.setValidator(QREVal(QRE("[0-9]{10}")))
        self.inn.setValidator(QREVal(QRE("[0-9]{8}")))
        self.snils.setValidator(QREVal(QRE("[0-9]{8}")))
        self.n_td.setValidator(QREVal(QRE("[0-9]{2}")))
        self.n_hght.setValidator(number_prot)
        self.n_study.setValidator(number_prot)
        self.n_study_card.setValidator(number_prot)
        self.n_prot.setValidator(number_prot)
        self.n_card.setValidator(number_prot)

    def _ev_select(self, text):
        for row in self.rows_from_db:
            if text in row:
                self.set_data(row)

    def clean_data(self):
        zero = Date.fromString("01.01.2000", "dd.mm.yyyy")
        self.passport_post.clear()
        self.adr.clear()
        self.live_adr.clear()

        self.family.setText("")
        self.name.setText("")
        self.surname.setText("")
        self.bday.setDate(zero)
        self.post.setText("")
        self.phone.setText("")
        self.passport.setText("")
        self.passport_post.append("")
        self.adr.append("")
        self.live_adr.append("")
        self.inn.setText("")
        self.snils.setText("")
        self.n_td.setText("")
        self.d_td.setDate(zero)
        self.n_hght.setText("")
        self.n_group_h.setText(str(0))
        self.d_height.setDate(zero)
        self.n_study.setText("")
        self.n_study_card.setText("")
        self.d_study.setDate(zero)
        self.n_prot.setText("")
        self.n_card.setText("")
        self.d_prot.setDate(zero)
        self.cb_contract.setCurrentIndex(0)
        pass

    def set_data(self, data):
        self.passport_post.clear()
        self.adr.clear()
        self.live_adr.clear()

        self.family.setText(data[1])
        self.family.enabled = False
        self.name.setText(data[0])
        self.surname.setText(data[2])
        self.bday.setDate(Date.fromString(data[3], "dd.mm.yyyy"))
        self.post.setText(data[4])
        self.phone.setText(data[5])
        self.passport.setText(data[6])
        self.passport_post.append(data[7])
        self.adr.append(data[8])
        self.live_adr.append(data[9])
        self.inn.setText(data[10])
        self.snils.setText(data[11])
        self.n_td.setText(data[12])
        self.d_td.setDate(Date.fromString(data[13], "dd.mm.yyyy"))
        self.n_hght.setText(data[14])
        self.n_group_h.setText(str(data[15]))
        self.d_height.setDate(Date.fromString(data[16], "dd.mm.yyyy"))
        self.n_study.setText(data[17])
        self.n_study_card.setText(data[18])
        self.d_study.setDate(Date.fromString(data[19], "dd.mm.yyyy"))
        self.n_prot.setText(data[20])
        self.n_card.setText(data[21])
        self.d_prot.setDate(Date.fromString(data[22], "dd.mm.yyyy"))

    def get_data(self):
        data = list([self.family.text(),
                    self.name.text(),
                    self.surname.text(),
                    self.bday.text(),
                    self.post.text(),
                    self.phone.text(),
                    self.passport.text(),
                    self.passport_post.toPlainText(),
                    self.adr.toPlainText(),
                    self.live_adr.toPlainText(),
                    self.inn.text(),
                    self.snils.text(),
                    self.n_td.text(),
                    self.d_td.text(),
                    self.n_hght.text(),
                    self.n_group_h.text(),
                    self.d_height.text(),
                    self.n_study.text(),
                    self.n_study_card.text(),
                    self.d_study.text(),
                    self.n_prot.text(),
                    self.n_card.text(),
                    self.d_prot.text(),
                    self.cb_contract.currentText()])
        if "" in data or "01.01.2000" in data:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return False
        return data

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_kill.setEnabled(False)
            self.family.setEnabled(True)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_kill.setEnabled(True)
            self.family.setEnabled(False)

    def my_update(self):
        try:
            data = self.get_data()
            if data:
                self.ev_kill()
                self.parent.get_new_data(data)
                self.close()
        except:
            print("error")
            return

