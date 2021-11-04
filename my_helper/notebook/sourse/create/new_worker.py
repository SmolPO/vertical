from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtWidgets import QMessageBox as mes
import datetime as dt
from my_helper.notebook.sourse.database import *
from my_helper.notebook.sourse.create.new_template import TempForm
designer_file = get_path_ui("new_worker")
covid = {"S5": 0, "SL": 1, "CV": 2}
msgs = {"mes": "Сообщение", "atn": "Внимание"}


class NewWorker(TempForm):
    def __init__(self, parent=None):
        super(NewWorker, self).__init__(designer_file, parent, "workers")
        if not self.status_:
            return
        # my_pass
        self.cb_auto.stateChanged.connect(self.ev_auto)
        self.cb_contract.activated[str].connect(self.select_contract)
        self.cb_vac.activated[str].connect(self.change_vac)
        self.init_mask()
        try:
            self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
            self.parent.db.init_list(self.cb_contract, "name", "contracts")
        except:
            mes.question(self, "Внимание", my_errors["2_get_path"], mes.Cancel)
            return
        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = -5
        self.current_id = self.next_id
        self.list_ui = list()
        self.auto_numbers = ()
        self.my_mem = ""

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
        return True

    def select_contract(self):
        pass

    def _clean_data(self):
        _zero = Date(*from_str(zero))
        list_ui = [[self.family, self.name, self.surname, self.post, self.phone, self.passport, self.inn,
                    self.snils, self.n_td, self.n_hght, self.n_study, self.n_study_card, self.n_prot,
                    self.n_card, self.vac_doc],
                   [self.bday, self.d_td, self.d_study, self.d_prot, self.d_vac_1, self.d_vac_2, self.d_height],
                   [self.passport_post, self.adr, self.live_adr]]
        for item in list_ui[0]:
            item.setText("")
        for item in list_ui[1]:
            item.setDate(Date(*from_str(zero)))
        for item in list_ui[2]:
            item.clear()
        self.n_group_h.setText(str(0))
        self.cb_contract.setCurrentIndex(0)
        self.status.setCurrentIndex(0)

    def _set_data(self, data):
        print(data)
        self.passport_post.clear()
        self.adr.clear()
        self.live_adr.clear()
        self.place.clear()

        self.family.setText(data[0])
        self.name.setText(data[1])
        self.surname.setText(data[2])
        self.bday.setDate(from_str(data[3]))
        self.post.setText(data[4])
        self.phone.setText(data[5])
        self.passport.setText(data[6])
        self.passport_post.append(data[7])
        self.adr.append(data[8])
        self.live_adr.append(data[9])

        self.inn.setText(data[10])
        self.snils.setText(data[11])

        self.n_td.setText(data[12])
        self.d_td.setDate(from_str(data[13]))

        self.n_hght.setText(data[14])
        self.n_group_h.setText(str(data[15]))
        self.d_height.setDate(from_str(data[16]))

        self.n_study.setText(data[17])
        self.n_study_card.setText(data[18])
        self.d_study.setDate(from_str(data[19]))

        self.n_prot.setText(data[20])
        self.n_card.setText(data[21])
        self.d_prot.setDate(from_str(data[22]))
        self.cb_contract.setCurrentIndex(int(data[23]))
        # vac
        self.set_vac_data(data[-6:-2])
        self.get_next_id(data)
        self.status.setCurrentIndex(statues.index(data[-2]))

    def change_vac(self):
        issue_type = 2
        sputnik_V = 0
        self.place.setEnabled(self.cb_vac.currentIndex() != issue_type)
        self.my_mem = self.place.toPlainText() if self.cb_vac.currentIndex() == issue_type else self.my_mem
        self.place.clear()
        self.place.append("нет" if self.cb_vac.currentIndex() == issue_type else self.my_mem)
        self.d_vac_2.setEnabled(True if self.cb_vac.currentIndex() == sputnik_V else False)

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

    def get_next_id(self, data):
        g = iter(range(len(self.rows_from_db) + 1))
        for item in self.rows_from_db:
            next(g)
            if data[-1] == item[-1]:
                self.cb_contract.setCurrentIndex(next(g))
                break

    def _get_data(self, data=None):
        vac = None
        data = list()

        list_ui = [self.family, self.name, self.surname, self.bday, self.post, self.phone, self.passport,
                   self.passport_post, self.adr, self.live_adr, self.inn, self.snils,
                   self.n_td, self.d_td,
                   self.n_hght, self.n_group_h, self.d_height,
                   self.n_study, self.n_study_card, self.d_study,
                   self.n_prot, self.n_card, self.d_prot]
        for item in list_ui:
            try:
                data.append(item.text())
            except:
                data.append(item.toPlainText())
        data.append(str(self.cb_contract.currentIndex()))
        data.append(self.d_vac_1.text())
        data.append(self.d_vac_2.text())
        data.append(self.place.toPlainText())
        for key in covid:
            if covid[key] == self.cb_vac.currentIndex():
                data.append(key + self.vac_doc.text())
                break
        data.append(str(self.status.currentText()))
        print(data)
        return data

    def check_input(self):
        data = list([self.family.text(), self.name.text(), self.surname.text(), self.bday.text(), self.post.text(),
                     self.phone.text(), self.passport.text(), self.passport_post.toPlainText(),
                     self.adr.toPlainText(), self.live_adr.toPlainText(), self.inn.text(), self.snils.text(),
                     self.n_td.text(), self.d_td.text(), self.n_hght.text(), self.n_group_h.text(),
                     self.d_height.text(), self.n_study.text(), self.n_study_card.text(), self.d_study.text(),
                     self.n_prot.text(), self.n_card.text(), self.d_prot.text(), self.status.currentText(),
                     self.cb_contract.currentText()])
        if not self.check_vac():
            return False
        if self.cb_check.isChecked():
            return msg(self, "Нет согласия на обработку персональных данных")
        if "" in data or zero in data or empty in data:
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

    def ev_auto(self, state):
        if state == 2:
            number = list()
            card = list()
            i = 0
            for worker in self.rows_from_db:
                print((i, worker))
                number.append(int(worker[20]))
                card.append(int(worker[21]))
            delta = 1 if dt.datetime.now().weekday() >= 1 else 3
            date = dt.datetime.now().date() - dt.timedelta(delta)
            if not number:
                number.append(0)
                card.append(0)
            self.auto_numbers = max(number), max(card), str(date)
            self.n_prot.setText(str(max(number) + 1))
            self.n_card.setText(str(max(card) + 1))
            self.d_prot.setDate(from_str(str(date)))

            self.n_prot.setEnabled(False)
            self.n_card.setEnabled(False)
            self.d_prot.setEnabled(False)
        else:
            self.n_prot.setEnabled(True)
            self.n_card.setEnabled(True)
            self.d_prot.setEnabled(True)

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True