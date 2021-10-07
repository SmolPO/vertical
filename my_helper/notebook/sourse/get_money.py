from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtCore import QDate as Date
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import Qt
from my_helper.notebook.sourse.inserts import get_from_db
designer_file = '../designer_ui/get_money_2.ui'


class GetMoney(QDialog):
    def __init__(self, parent):
        super(GetMoney, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.bosses = []
        self.table = "finance"
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)

        self.cb_recipient.activated[str].connect(self.change_note)
        self.cb_select.activated[str].connect(self.ev_select)
        # self.cb_manual_set.stateChanged.connect(self.manual_set)
        self.cb_day.stateChanged.connect(self.day_money)

        self.note.textChanged.connect(self.change_note)
        self.sb_value.valueChanged[int].connect(self.change_note)
        self.sb_days.valueChanged[int].connect(self.change_note)
        self.sb_emploeeyrs.stateChanged.connect(self.change_note)
        self.sb_cost.stateChanged.connect(self.change_note)
        self.cb_some.stateChanged.connect(self.change_note)
        self.cb_day.stateChanged.connect(self.change_note)

        # self.but_status("add")
        self.rows_from_db = self.from_db("*", self.table)
        self.cb_select.addItems(["(нет)"])
        for row in self.rows_from_db:
            self.cb_chouse.addItems([", ".join((row[0], row[1]))])

        self.cb_recipient.addItems(["(нет)"])
        for row in self.from_db("family, name", "itrs"):
            self.cb_recipient.addItems([" ".join((row[0], row[1][0])) + "."])
        self.my_id.setValue(self.next_id())

    def ev_ok(self):
        data = self.get_data()
        if not data:
            return
        self.parent.get_new_data(data)
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_select(self, text):
        if text == "(нет)":
            self.clean_data()
            self.but_status("add")
            return
        else:
            self.but_status("change")

        for row in self.rows_from_db:
            if text in row:
                self.set_data(row)

    def change_note(self, state=None):
        itr = ""
        people = self.from_db("post, family, name", "itrs")
        for boss in people:
            if self.cb_recipient.currentText()[:-4] in boss:
                itr = boss
        text = list()
        text.append("Прошу Вас выслать ")
        text.append(str(self.sb_value.value()))
        text.append(" на банковскую карту ")
        text.append(" ".join(itr[0:2]))
        text.append(" для:\n")
        if self.cb_day.isChecked():
            text.append("- суточные {0} чел {1} дней {2}р. ставка\n".format(self.sb_days.value(),
                                                                            self.sb_emploeeyrs.value(),
                                                                            self.sb_cost.value()))
        if self.cb_some.isChecked():
            text.append("- производственные нужды\n")
        text.append(" - " + self.note.toPlainText())
        self.note_result.setText(" ".join(text))

    def day_money(self, state):
        if state == Qt.Checked:
            self.sb_days.setEnabled(True)
            self.sb_emploeeyrs.setEnabled(True)
            self.sb_cost.setEnabled(True)
        else:
            self.sb_daysm.setEnabled(False)
            self.sb_emploeeyrs.setEnabled(False)
            self.sb_cost.setEnabled(False)

# def manual_set(self, state):
#   status = True if state == Qt.Checked else False
#   self.note_result.setEnabled(status)

    def ev_change(self):
        for row in self.rows_from_db:
            if self.my_id.value() in row:
                self.my_update()
                print("update")
        pass

    def ev_kill(self):
        for row in self.rows_from_db:
            if self.my_id.text() in row:
                data = self.get_data()
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    print("DELETE FROM {0} WHERE id = '{1}'".format(
                        self.table, self.my_id.value()))
                    print(row)
                    self.parent.db.execute("DELETE FROM {0} WHERE id = '{1}'".format(
                        self.table, self.my_id.value()))
                    self.parent.db_conn.commit()
                    self.close()
                    return
                if answer == QMessageBox.Cancel:
                    return

    def set_data(self, data):
        self.sb_number.setValue(data[0])
        self.date.setDate(Date.fromString(data[1], "dd.mm.yyyy"))
        self.sb_value.Value(int(data[2]))
        i = range(len(self.rows_from_db))
        for row in self.rows_from_db:
            self.cb_recipient.setCurrentIndex(next(i)) if data[3] in row else next(i)
        self.note.clear()
        self.note.append(data[4])

    def get_data(self):
        data = list()
        data.append(str(self.my_id_.value()))
        data.append(self.date.text())
        data.append(str(self.sb_value.value()))
        data.append(self.cb_recipient.currentText())
        if self.cb_day.setChecked():
            data.append("суточные {0} чел {1} дней {2}р. ставка".format(self.sb_days.value(),
                                                                        self.sb_emploeers.value(),
                                                                        self.sb_cost.value))
        if self.note.toPlainText():
            if len(data) == 3:
                data.append("производственные нужды")
            else:
                data[4] = data[4] + "| производственные нужды"
        if self.cb_some.setChecked():
            if len(data) == 3:
                data.append(self.note.toPlainText())
            else:
                data[4] = data[4] + "| " + self.note.toPlainText()
        return data

    def check_input(self):
        if "" in list([self.sb_value.value(),
                     self.name.text(),
                     self.surname.text(),
                     self.post.text()]):
            return False
        return True

    def clean_data(self):
        self.sb_recipient.setCurrentIndex(0)
        self.sb_value.setValue(0)
        self.note.clear()
        self.cb_day.setCheacked(False)
        self.sb_day.setValue(0)
        self.sb_emploeers.setValue(0)

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_kill.setEnabled(False)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_kill.setEnabled(True)

    def my_update(self):
        self.ev_kill()
        self.parent.get_new_data(self.get_data())
        self.close()
        pass

    def next_id(self):
        if not self.rows_from_db:
            return 1
        else:
            return str(int(self.rows_from_db[-1][0]) + 1)

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()
