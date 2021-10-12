from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.new_template import TempForm, from_str
from PyQt5.QtWidgets import QMessageBox as mes
designer_file = '../designer_ui/new_itr.ui'


class NewITR(TempForm):
    def __init__(self, parent):
        super(NewITR, self).__init__(designer_file)
        # pass
        self.parent = parent
        self.table = "itrs"
        self.init_mask()
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = -5
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id
        self.list_ui = list()

    def init_mask(self):
        list_valid = [[self.family,  self.name, self.surname, self.post], [self.n_OT_p, self.n_OT_c, self.n_PTM_p,
                                                                            self.n_PTM_c, self.n_ES_p,  self.n_ES_c,
                                                                            self.n_H_p, self.n_H_c, self.n_ST_p,
                                                                            self.n_ST_c]]
        for item in list_valid[0]:
            item.setValidator(QREVal(QRE("[а-яА-Я]{30}")))
        for item in list_valid[1]:
            item.setValidator(QREVal(QRE("[А-Яа-я /- 0-9]{10}")))

        self.passport.setValidator(QREVal(QRE("[0-9]{10}")))
        self.inn.setValidator(QREVal(QRE("[0-9]{9}")))
        self.snils.setValidator(QREVal(QRE("[0-9]{11}")))
        self.n_td.setValidator(QREVal(QRE("[0-9]{3}")))
        self.n_ES_g.setValidator(QREVal(QRE("[0-9]{3}")))
        self.n_H_g.setValidator(QREVal(QRE("[0-9]{3}")))

    def _clean_data(self):
        list_clean = [[self.family, self.name, self.surname, self.post, self.my_auto, self.passport, self.inn,
                       self.snils, self.n_td, self.n_OT_p, self.n_OT_c, self.n_PTM_p, self.n_PTM_c, self.n_ES_p,
                       self.n_ES_c, self.n_ES_g, self.n_H_p, self.n_H_c, self.n_H_g, self.n_ST_p, self.n_ST_c],
                      [self.bday, self.passport_date, self.d_td, self.d_OT, self.d_PTM, self.d_ES, self.d_H,
                       self.d_ST], [self.passport_got, self.live_adr, self.promsave]]
        for item in list_clean[0]:
            item.setText("")
        for item in list_clean[1]:
            item.setDate(Date(from_str("01.01.2000")))
        for item in list_clean[2]:
            item.clear()

    def _set_data(self, data):
        self.promsave.clear()
        self.adr.clear()
        self.live_adr.clear()
        self.passport_got.clear()
        print(data)

        self.family.setText(data[0])
        self.name.setText(data[1])
        self.surname.setText(data[2])
        self.post.setText(data[3])

        self.passport.setText((data[4]))
        self.passport_date.setDate(Date(from_str(data[5])))
        self.passport_got.append(data[6])
        self.adr.append(data[7])
        self.live_adr.append(data[8])
        self.my_auto.setText(data[9])

        self.inn.setText((data[10]))
        self.snils.setText((data[11]))
        self.n_td.setText((data[12]))
        self.d_td.setDate(Date(from_str(data[13])))

        self.n_OT_p.setText((data[14]))
        self.d_OT.setDate(Date(from_str(data[15])))
        self.n_OT_c.setText((data[16]))

        self.n_PTM_p.setText((data[17]))
        self.d_PTM.setDate(Date(from_str(data[18])))
        self.n_PTM_c.setText((data[19]))

        self.n_ES_p.setText((data[20]))
        self.n_ES_g.setText((data[21]))
        self.n_ES_c.setText((data[22]))
        self.d_ES.setDate(Date(from_str(data[23])))

        self.n_H_p.setText((data[24]))
        self.d_H.setDate(Date(from_str(data[25])))
        self.n_H_g.setText((data[26]))
        self.n_H_c.setText((data[27]))

        self.promsave.append(data[28])

        self.n_ST_p.setText((data[29]))
        self.n_ST_c.setText((data[30]))
        self.d_ST.setDate(Date(from_str(data[31])))
        self.bday.setDate(Date(from_str(data[32])))

    def _get_data(self, data):
        _data = list([self.family.text(), self.name.text(), self.surname.text(),
                      self.post.text(), self.passport.text(), self.passport_date.text(),
                      self.passport_got.toPlainText(), self.adr.toPlainText(),
                      self.live_adr.toPlainText(), self.my_auto.text(),
                      self.inn.text(), self.snils.text(),
                      self.n_td.text(), self.d_td.text(),
                      self.n_OT_p.text(), self.d_OT.text(), self.n_OT_c.text(),
                      self.n_PTM_p.text(), self.d_PTM.text(), self.n_PTM_c.text(),
                      self.n_ES_p.text(), self.n_ES_g.text(), self.n_ES_c.text(), self.d_ES.text(),
                      self.n_H_p.text(), self.d_H.text(), self.n_H_g.text(),  self.n_H_c.text(),
                      self.promsave.toPlainText(),
                      self.n_ST_p.text(), self.n_ST_c.text(), self.d_ST.text(),
                      self.bday.text()])
        return _data

    def check_input(self):
        _data = list([self.family.text(), self.name.text(), self.surname.text(),
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
        if "" in _data or "01.01.2000" in _data or "(нет)" in _data:
            mes.question(self, "Сообщение", "Заполните все поля", mes.Cancel)
            return False
        else:
            return True

    def _ev_select(self, text):
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True