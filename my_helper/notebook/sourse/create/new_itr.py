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
        self.cb_vac.activated[str].connect(self.change_vac)
        try:
            self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
            self.parent.db.init_list(self.cb_auto, "*", "auto")
        except:
            msg(self, my_errors["3_get_db"])
            return
        """
        (family, name, surname, post, passport, passport_date, passport_got, adr, live_adr, auto, inn, "
       "snils, n_employment_contract,date_employment_contract, "
       "ot_protocol, ot_date, ot_card, "
       "PTM_protocol, PTM_date, PTM_card, "
       "es_protocol, es_group, es_card, es_date, "
       "h_protocol, h_date, h_group, h_card, "
       "industrial_save, "
       "st_protocol, st_card, st_date, birthday, "
       " d_vac_1, d_vac_2, place, vac_doc, vac_type, status, id)",
        """
        self.list_ui = [self.family, self.name, self.surname, self.post, self.passport, self.passport_date,
                        self.passport_got, self.adr, self.live_adr, self.inn,
                        self.snils, self.n_td, self.d_td, self.n_OT_p, self.d_OT, self.n_OT_c,
                        self.n_PTM_p, self.d_PTM, self.n_PTM_c,
                        self.n_ES_p, self.n_ES_g, self.n_ES_c, self.d_ES,
                        self.n_H_p, self.d_H, self.n_H_g, self.n_H_c,
                        self.promsave,
                        self.n_ST_p, self.n_ST_c, self.d_ST,
                        self.bday,
                        self.d_vac_1, self.d_vac_2, self.place, self.vac_doc, self.cb_vac, self.status]
        self.my_mem = ""
        self.vac = True

    def _select(self, text):
        return True

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
        self.status.setCurrentIndex(int(data[-2]))
        self.set_vac_data(data[-6:-2])
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
        print(data)
        self.d_vac_1.setDate(from_str(data[0]))
        self.vac_doc.setText(data[3][2:])
        self.cb_vac.setCurrentIndex(covid[data[3][:2]])
        if data[3][0:2] == "S5":
            self.d_vac_2.setDate(from_str(data[1]))
            self.place.append(data[2])
        elif data[3][0:2] == "SL":
            self.d_vac_2.setDate(zero)
            self.d_vac_2.setEnabled(False)
            self.place.append(data[2])
        elif data[3][0:2] == "CV":
            self.d_vac_2.setDate(zero)
            self.place.clear()
            self.d_vac_2.setEnabled(False)
            self.place.setEnabled(False)

    def change_vac(self):
        issue_type = 2
        sputnik_V = 0
        self.place.setEnabled(self.cb_vac.currentIndex() != issue_type)
        self.my_mem = self.place.toPlainText() if self.cb_vac.currentIndex() == issue_type else self.my_mem
        self.place.clear()
        self.place.append("нет" if self.cb_vac.currentIndex() == issue_type else self.my_mem)
        self.d_vac_2.setEnabled(True if self.cb_vac.currentIndex() == sputnik_V else False)

    def _get_data(self, data):
        if self.cb_auto.currentText() == empty:
            auto = empty
        else:
            auto = self.cb_auto.currentText().split(". ")[1]
        print(auto)
        vac = None
        for key in covid:
            if covid[key] == self.cb_vac.currentIndex():
                vac = key + self.vac_doc.text()
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
                      self.d_vac_1.text(), self.d_vac_2.text(), self.place.toPlainText(), vac,
                      str(self.status.currentIndex())])
        return _data

    def check_input(self):
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
