from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.database import *
from my_helper.notebook.sourse.create.new_template import TempForm
covid = {"S5": 0, "SL": 1, "CV": 2}
msgs = {"mes": "Сообщение", "atn": "Внимание"}
designer_file = get_path_ui("new_itr")


class NewITR(TempForm):
    def __init__(self, parent):
        super(NewITR, self).__init__(designer_file, parent, "itrs")
        if not self.status_:
            return
        # my_pass
        self.init_mask()
        try:
            self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
            self.parent.db.init_list(self.cb_auto, "*", "auto")
        except:
            msg(self, my_errors["3_get_db"])
            return
        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = -5
        self.current_id = self.next_id
        self.list_ui = list()

    def init_mask(self):
        list_valid = [[self.family,  self.name, self.surname, self.post],
                      [self.n_OT_p, self.n_OT_c, self.n_PTM_p, self.n_PTM_c, self.n_ES_p,  self.n_ES_c,
                       self.n_H_p, self.n_H_c, self.n_ST_p, self.n_ST_c]]
        for item in list_valid[0]:
            item.setValidator(QREVal(QRE("[а-яА-Я ]{30}")))
        for item in list_valid[1]:
            item.setValidator(QREVal(QRE("[А-Яа-я /- 0-9]{10}")))

        self.passport.setValidator(QREVal(QRE("[0-9]{10}")))
        self.inn.setValidator(QREVal(QRE("[0-9]{9}")))
        self.snils.setValidator(QREVal(QRE("[0-9]{11}")))
        self.n_td.setValidator(QREVal(QRE("[0-9]{3}")))
        self.n_ES_g.setValidator(QREVal(QRE("[0-9]{3}")))
        self.n_H_g.setValidator(QREVal(QRE("[0-9]{3}")))

    def _clean_data(self):
        list_clean = [[self.family, self.name, self.surname, self.post, self.passport, self.inn,
                       self.snils, self.n_td, self.n_OT_p, self.n_OT_c, self.n_PTM_p, self.n_PTM_c, self.n_ES_p,
                       self.n_ES_c, self.n_ES_g, self.n_H_p, self.n_H_c, self.n_H_g, self.n_ST_p, self.n_ST_c,
                       self.vac_doc],
                      [self.bday, self.passport_date, self.d_td, self.d_OT,
                       self.d_PTM, self.d_ES, self.d_H, self.d_ST, self.d_vac_1, self.d_vac_2],
                      [self.passport_got, self.live_adr, self.promsave, self.place]]
        self.cb_contract.setCurrentIndex(0)
        for item in list_clean[0]:
            item.setText("")
        for item in list_clean[1]:
            item.setDate(Date(*from_str(zero)))
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
        self.passport_date.setDate(from_str(data[5]))
        self.passport_got.append(data[6])
        self.adr.append(data[7])
        self.live_adr.append(data[8])

        self.inn.setText((data[10]))
        self.snils.setText((data[11]))
        self.n_td.setText((data[12]))
        self.d_td.setDate(from_str(data[13]))

        self.n_OT_p.setText((data[14]))
        self.d_OT.setDate(from_str(data[15]))
        self.n_OT_c.setText((data[16]))

        self.n_PTM_p.setText((data[17]))
        self.d_PTM.setDate(from_str(data[18]))
        self.n_PTM_c.setText((data[19]))

        self.n_ES_p.setText((data[20]))
        self.n_ES_g.setText((data[21]))
        self.n_ES_c.setText((data[22]))
        self.d_ES.setDate(from_str(data[23]))

        self.n_H_p.setText((data[24]))
        self.d_H.setDate(from_str(data[25]))
        self.n_H_g.setText((data[26]))
        self.n_H_c.setText((data[27]))

        self.promsave.append(data[28])

        self.n_ST_p.setText((data[29]))
        self.n_ST_c.setText((data[30]))
        self.d_ST.setDate(from_str(data[31]))
        self.bday.setDate(from_str(data[32]))
        self.set_vac_data(data)

        try:
            list_auto = self.parent.db.get_data("*", "auto")
        except:
            return msg(self, my_errors["3_get_db"])
        g = iter(range(len(list_auto) + 1))
        for item in list_auto:
            next(g)
            if data[9] == item[0]:
                self.cb_auto.setCurrentIndex(next(g))
                break

    def set_vac_data(self, data):
        _zero = Date(from_str(zero))
        self.d_vac_1.setDate(from_str(data[-6]))
        self.vac_doc.setText(data[-3][2:])
        self.cb_vac.setCurrentIndex(covid[data[-3][:2]])
        if data[-3][0:1] == "S5":
            self.d_vac_2.setDate(from_str(data[-5]))
            self.place.append(data[-4])
        elif data[-3][0:1] == "SL":
            self.d_vac_2.setDate(_zero)
            self.d_vac_2.setEnabled(False)
            self.place.append(data[-4])
        elif data[-3][0:1] == "CV":
            self.d_vac_2.setDate(_zero)
            self.place.clean()
            self.d_vac_2.setEnabled(False)
            self.place.setEnabled(False)

    def _get_data(self, data):
        if self.cb_auto.currentText() == empty:
            auto = empty
        else:
            auto = self.cb_auto.currentText().split(". ")[1]
        print(auto)
        vac = None
        for key in covid:
            if covid[key] == self.cb_vac.CurrentIndex():
                vac = key + self.self.cb_vac.currentText()
        _data = list([self.family.text(), self.name.text(), self.surname.text(),
                      self.post.text(), self.passport.text(), self.passport_date.text(),
                      self.passport_got.toPlainText(), self.adr.toPlainText(),
                      self.live_adr.toPlainText(), auto,
                      self.inn.text(), self.snils.text(),
                      self.n_td.text(), self.d_td.text(),
                      self.n_OT_p.text(), self.d_OT.text(), self.n_OT_c.text(),
                      self.n_PTM_p.text(), self.d_PTM.text(), self.n_PTM_c.text(),
                      self.n_ES_p.text(), self.n_ES_g.text(), self.n_ES_c.text(), self.d_ES.text(),
                      self.n_H_p.text(), self.d_H.text(), self.n_H_g.text(),  self.n_H_c.text(),
                      self.promsave.toPlainText(),
                      self.n_ST_p.text(), self.n_ST_c.text(), self.d_ST.text(),
                      self.bday.text(),
                      self.d_vac_1.text(), self.d_vac_2.text(),self.plase.toPlainText(), vac])
        return _data

    def check_input(self):
        list_ui = [self.family, self.name, self.surname, self.post, self.passport, self.passport_date,
                   self.passport_got, self.adr, self.live_adr, self.inn, self.snils, self.n_td, self.d_td,
                   self.n_OT_p, self.n_OT_c, self.d_OT, self.n_PTM_p, self.n_PTM_c, self.d_PTM, self.n_ES_p,
                   self.n_ES_c, self.n_ES_g, self.d_ES, self.n_H_p, self.n_H_c, self.n_H_g, self.d_H,
                   self.n_ST_p, self.n_ST_c, self.d_ST, self.promsave, self.bday]
        _data = list()
        for item in list_ui:
            try:
                _data.append(item.text())
            except:
                _data.append(item.toPlainText())
        if not self.check_vac():
            return False
        if ("" in _data) or ("01.01.2000") in (_data or empty in _data):
           return msg(self, "Заполните все поля")
        else:
            return True

    def check_vac(self):
        list_vac = [self.d_vac_1.text(), self.d_vac_2.text(), self.place.toPlainText(),
                    self.vac_doc.text(), self.cb_vac.currentIndex()]
        m_val = {"year": 6, "type": -1, "SputnikV": 0, "Lite": 1, "issue": 2, "d_vac_1": 0, "d_vac_2": 1,
                 "min_len": 3, "place": 2, "doc": 3}  # магические переменные
        try:
            vac_safe = int(get_config("vac_safe"))
            vac_do = int(get_config("vac_do"))
            vac_days = int(get_config("vac_days"))
            cv_safe = int(get_config("cv_safe"))
        except:
            return msg(self, my_errors["2_get_ini"])

        if list_vac[m_val["type"]] == m_val["SputnikV"]:

            if len(list_vac[m_val["place"]]) < m_val["min_len"]:
                return msg(self, "Укажите место прививки")

            if time_delta("now", list_vac[m_val["d_vac_2"]]) > vac_safe:
                return msg(self, "Сертификат устарел. С даты прививки прошло более " + str(vac_safe) + " дней.")

            delta = time_delta(list_vac[m_val["d_vac_2"]], list_vac[m_val["d_vac_1"]])
            if delta < vac_days:
                return msg(self, "Между прививками прошло " + str(delta) + " дней. "
                                                                           "Это менее " + str(vac_days) + " дней")

            if delta > vac_do:
                return msg(self, "Между прививками прошло " + str(delta) + "дней. "
                                                                           "Это более " + str(vac_do) + " дней.")

        elif list_vac[m_val["type"]] == m_val["Lite"]:

            if len(list_vac[m_val["place"]]) < m_val["min_len"]:
                return msg(self, "Укажите место прививки")

            if time_delta("now", list_vac[m_val["d_vac_1"]]) > vac_safe:
                return msg(self, "Сертификат устарел. С даты прививки прошло более " + str(vac_safe) + " дней.")

        elif list_vac[m_val["type"]] == m_val["issue"]:

            if len(list_vac[m_val["doc"]]) < m_val["min_len"]:
                return msg(self, "Укажите номер сертификата")

            if time_delta("now", list_vac[m_val["d_vac_1"]]) > cv_safe:
                return msg(self, "Сертификат устарел, необходима вакцинация")
        return True

    def _ev_select(self, text):
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True