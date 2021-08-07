from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal

fields = ["family", "name", "surname", "post",
          "passport", "passport_date", "passport_got",
          "adr", "live_adr",
          "auto", "inn", "snils",
          "n_td", "td_date",
          "OT_prot", "OT_card", "OT_date",
          "PTM_prot", "PTM_card", "PTM_date",
          "ES_prot", "ES_group", "ES_card", "ES_date",
          "H_prot", "H_group", "H_card", "H_date",
          "ST_prot", "ST_card", "ST_date", "promsave", "birthday"]

class NewITR(QDialog):
    def __init__(self, parent):
        super(NewITR, self).__init__()
        uic.loadUi('../designer_ui/new_itr.ui', self)
        # pass
        self.parent = parent
        self.itr = []
        self.table = "itr"
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_del.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_chouse.activated[str].connect(self.ev_select)
        self.but_status("add")
        self.init_mask()
        self.cb_chouse.addItems(["(нет)"])
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        for row in self.parent.database_cur.fetchall():
            self.cb_chouse.addItems([row[0]])

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я]{30}"))
        number_prot = QREVal(QRE("[А-Яа-я /- 0-9]{10}"))

        self.family.setValidator(symbols)
        self.name.setValidator(symbols)
        self.surname.setValidator(symbols)
        self.post.setValidator(symbols)

        self.passport.setValidator(QREVal(QRE("[0-9]{10}")))
        #  self.passport_got.clear()
        #  self.adr.clear()
        #  self.live_adr.clear()
        self.inn.setValidator(QREVal(QRE("[0-9]{9}")))
        self.snils.setValidator(QREVal(QRE("[0-9]{11}")))
        self.n_td.setValidator(QREVal(QRE("[0-9]{3}")))

        self.n_OT_p.setValidator(number_prot)
        self.n_OT_c.setValidator(number_prot)

        self.n_PTM_p.setValidator(number_prot)
        self.n_PTM_c.setValidator(number_prot)

        self.n_ES_p.setValidator(number_prot)
        self.n_ES_c.setValidator(number_prot)
        self.n_ES_g.setValidator(QREVal(QRE("[0-9]{3}")))

        self.n_H_p.setValidator(number_prot)
        self.n_H_c.setValidator(number_prot)
        self.n_H_g.setValidator(QREVal(QRE("[0-9]{3}")))

        self.n_ST_p.setValidator(number_prot)
        self.n_ST_c.setValidator(number_prot)

    def ev_OK(self):
        self.parent.get_new_itr(self.get_data())
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_select(self, text):
        if text == "(нет)":
            self.clear()
            self.but_status("add")
            return
        else:
            self.but_status("change")

        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if text in row:
                self.set_data(row)

    def ev_change(self):
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if self.family.text() in row and self.name.text() in row:
                self.my_update()
                print("update")
        pass

    def ev_kill(self):
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if self.family.text() in row:
                data = self.get_data()
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.database_cur.execute("DELETE FROM {0} WHERE family = '{1}'".format(
                        self.table, self.family.text()))
                    self.parent.database_conn.commit()  # TODO удаление
                    self.close()
                    return
                if answer == QMessageBox.Cancel:
                    return

    def clear(self):
        self.family.setText("")
        self.name.setText("")
        self.surname.setText("")
        self.post.setText("")
        self.bday.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))
        self.my_auto.setText("")
        self.passport.setText("")
        self.passport_got.clear()
        self.passport_date.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))
        self.adr.clear()
        self.live_adr.clear()
        self.inn.setText("")
        self.snils.setText("")
        self.n_td.setText("")
        self.d_td.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))

        self.n_OT_p.setText("")
        self.n_OT_c.setText("")
        self.d_OT.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))

        self.n_PTM_p.setText("")
        self.n_PTM_c.setText("")
        self.d_PTM.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))

        self.n_ES_p.setText("")
        self.n_ES_c.setText("")
        self.n_ES_g.setText("")
        self.d_ES.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))

        self.n_H_p.setText("")
        self.n_H_c.setText("")
        self.n_H_g.setText("")
        self.d_H.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))

        self.n_ST_p.setText("")
        self.n_ST_c.setText("")
        self.d_ST.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))

        self.promsave.clear()

    def set_data(self, data):
        self.promsave.clear()
        self.adr.clear()
        self.live_adr.clear()
        self.passport_got.clear()

        self.family.setText(data[fields.index("family")])
        self.name.setText(data[fields.index("name")])
        self.surname.setText(data[fields.index("surname")])
        self.post.setText(data[fields.index("post")])
        date_str = data[fields.index("birthday")]
        qdate = QtCore.QDate.fromString(date_str, "dd.mm.yyyy")
        self.bday.setDisplayFormat("dd.mm.yyyy")
        self.bday.setDate(qdate)
        self.my_auto.setText(data[fields.index("auto")])
        self.promsave.append(data[fields.index("promsave")])
        self.adr.append(data[fields.index("adr")])
        self.live_adr.append(data[fields.index("live_adr")])
        self.passport_got.append(data[fields.index("passport_got")])

        self.passport.setText((data[fields.index("passport")]))
        self.passport_date.setDate(Date.fromString(data[fields.index("post")]))

        self.inn.setText((data[fields.index("inn")]))
        self.snils.setText((data[fields.index("snils")]))
        self.n_td.setText((data[fields.index("n_td")]))
        self.d_td.setDate(Date.fromString(data[fields.index("td_date")]))

        self.n_OT_p.setText((data[fields.index("OT_prot")]))
        self.n_OT_c.setText((data[fields.index("OT_card")]))
        self.d_OT.setDate(Date.fromString((data[fields.index("OT_date")])))

        self.n_PTM_p.setText((data[fields.index("PTM_prot")]))
        self.n_PTM_c.setText((data[fields.index("PTM_card")]))
        self.d_PTM.setDate(Date.fromString((data[fields.index("PTM_date")])))

        self.n_ES_p.setText((data[fields.index("ES_prot")]))
        self.n_ES_c.setText((data[fields.index("ES_card")]))
        self.n_ES_g.setText((data[fields.index("ES_group")]))
        self.d_ES.setDate(Date.fromString((data[fields.index("ES_date")])))

        self.n_H_p.setText((data[fields.index("H_prot")]))
        self.n_H_c.setText((data[fields.index("H_card")]))
        self.n_H_g.setText((data[fields.index("H_group")]))
        self.d_H.setDate(Date.fromString((data[fields.index("H_group")])))

        self.n_ST_p.setText((data[fields.index("ST_prot")]))
        self.n_ST_c.setText((data[fields.index("ST_card")]))
        self.d_ST.setDate(Date.fromString((data[fields.index("ST_card")])))

    def get_data(self):
        names_tables = "(family, name, surname, post, passport, passport_date, passport_got, adr, live_adr, auto, inn, " \
                       "snils, n_td, td_date, " \
                       "ot_prot, ot_card, ot_date, " \
                       "PTM_prot, PTM_card, PTM_date, " \
                       "es_prot, es_group, es_card, es_date, " \
                       "h_prot, h_group, h_card, h_date, " \
                       "promsave, " \
                       "st_prot, st_card, st_date, birthday)"
        data = list([self.family.text(), self.name.text(), self.surname.text(),
                    self.post.text(), self.passport.text(), self.passport_date.text(),
                    self.passport_got.toPlainText(), self.adr.toPlainText(),
                    self.live_adr.toPlainText(), self.my_auto.text(),
                    self.inn.text(), self.snils.text(),
                    self.n_td.text(), self.d_td.text(),

                    self.n_OT_p.text(), self.n_OT_c.text(), self.d_OT.text(),

                    self.n_PTM_p.text(), self.n_PTM_c.text(), self.d_PTM.text(),

                    self.n_ES_p.text(), self.n_ES_c.text(), self.n_ES_g.text(), self.d_ES.text(),

                    self.n_H_p.text(), self.n_H_c.text(), self.n_H_g.text(), self.d_H.text(),

                    self.n_ST_p.text(), self.n_ST_c.text(), self.d_ST.text(),

                    self.promsave.toPlainText(),

                    self.bday.text()])
        return data

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_del.setEnabled(False)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_del.setEnabled(True)

    def my_update(self):
        self.ev_kill()
        self.parent.get_new_itr(self.get_data())
        self.close()
        pass

