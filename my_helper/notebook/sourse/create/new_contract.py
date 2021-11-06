from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtWidgets import QMessageBox as mes
import os
import PyPDF2
from my_helper.notebook.sourse.create.new_template import TempForm
from my_helper.notebook.sourse.database import *
from my_helper.notebook.sourse.acts.journal import Journal
from my_helper.notebook.sourse.acts.report import CreateReport

# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("new_contract")
fields = ["name", "customer", "number", "date", "object", "type_work", "place", "id"]
statues_cntr = ["Начат", "Заершен"]
_zero = "01.01.2000"


class NewContact(TempForm):
    def __init__(self, parent=None):
        super(NewContact, self).__init__(designer_file, parent, "contracts")
        if not self.status_:
            return
        self.init_mask()
        self.b_docs.clicked.connect(self.create_docs)
        self.b_menu.clicked.connect(self.start_menu)
        self.cb_select.activated[str].connect(self._ev_select)
        try:
            self.parent.db.init_list(self.cb_select, "name, id", self.table)
        except:
            msg(self, my_errors["3_get_db"])
            return
        self.list_ui = [self.name, self.cb_comp, self.part, self.number, self.date, self.my_object, self.work]

        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = len(self.list_ui)
        self.current_id = self.next_id
        self.cb_comp.addItem(self.parent.customer)
        self.b_menu.setEnabled(False)

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я ]{30}"))
        self.name.setValidator(symbols)
        self.number.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.part.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.price.setValidator(QREVal(QRE("[,0-9]{1000}")))

    def _ev_select(self, text):
        if text == empty:
            self.clean_data()
            self.but_status("add")
            self.current_id = self.next_id
            self.b_menu.setEnabled(False)
            return
        else:
            self.but_status("change")
            self.b_menu.setEnabled(True)

        for row in self.rows_from_db:
            if text.split(".")[0] == str(row[-1]):
                self.set_data(row)
                return

    def _clean_data(self):
        list_ui = [self.name, self.part, self.number]
        for item in list_ui:
            item.setText("")
        self.cb_comp.setCurrentIndex(0)
        self.date.setDate(zero)
        self.my_object.clear()
        self.work.clear()
        self.date_end.setDate(zero)
        self.price.setText("")
        self.NDS.setChecked(True)
        self.avans.setValue(0)

    def _set_data(self, data):
        """
        "(name, customer, number, date, object, type_work, place, "
                        "price, date_end, nds, avans, status, id)"
        :param data:
        :return:
        """
        self.my_object.clear()
        self.work.clear()
        self.name.setText(data[0])
        g = iter(range(len(self.rows_from_db) + 1))
        for item in self.rows_from_db:
            next(g)
            if data[-1] == item[-1]:
                self.cb_comp.setCurrentIndex(next(g))
                break
        self.number.setText(data[2])
        self.date.setDate(from_str(data[3]))
        self.my_object.append(data[4])
        self.work.append(data[5])
        self.part.setText(data[6])
        self.price.setText(data[7])
        self.date_end.setDate(from_str(data[8]))
        self.NDS.setChecked(True) if data[9] == "да" else self.NDS.setChecked(False)
        self.avans.setValue(int(data[10]))
        self.status.setCurrentIndex(statues_cntr.index(data[-2]))
        self.current_id = data[-1]
        path_docs = get_path("path") + get_path("path_contracts")
        self.path = path_docs + "/" + self.number.text()

    def _get_data(self, data):
        data.append(self.name.text())
        data.append(self.cb_comp.currentText())
        data.append(self.number.text())
        data.append(self.date.text())
        data.append(self.my_object.toPlainText())
        data.append(self.work.toPlainText())
        data.append(self.part.text())
        data.append(self.price.text())
        data.append(self.date_end.text())
        data.append("да" if self.NDS.isChecked() else "нет")
        data.append(str(self.avans.value()))
        data.append(self.status.currentText())
        return data

    def create_docs(self):
        if not self.check_input():
            return
        contract = str(self.number.text())
        path_docs = get_path("path") + get_path("path_contracts")
        self.path = path_docs + "/" + contract
        folders = self.check_folder(contract, path_docs)
        if folders:
            for item in folders:
                os.mkdir(self.path + item)
        self.create_doc()
        self.create_journal()
        self.create_acts()

    def check_folder(self, contract, path):
        path_docs = path + "/" + contract
        _folders = ["", "/Документы", "/Документы/ППР", "/Документы/Договор", "/Документы/Приложение",
                    "/Документы/Приложение/Фото", "/Документы/Приложение/Накладные"]
        folders = []
        current_folder = os.listdir(path)
        if not contract in current_folder:
            return _folders
        else:
            current_folder = os.listdir(path_docs)
            if not "Документы" in current_folder:
                return _folders[1:]
            current_folder = os.listdir(path_docs + "/Документы")
            if not "ППР" in current_folder:
                folders.append(_folders[2])
            if not "Договор" in current_folder:
                folders.append(_folders[3])
            if not "Приложение" in current_folder:
                return _folders[4:]
            else:
                current_folder = os.listdir(path_docs + "/Документы/Приложение")
                if not "Фото" in current_folder:
                    folders.append(_folders[5])
                if not "Накладные" in current_folder:
                    folders.append(_folders[6])
        return folders
        pass

    def create_doc(self):
        folder = get_path("path") + get_path("path_scan")
        types = ["Договор", "ЕКР", "Дефектная", "Материалы"]
        for file in types:
            answer = mes.question(self, "Добавление " + file,
                                  "Отсканируйте " + file + " в PDF по порядку и затем нажмите ОК. ",
                                  mes.Ok | mes.Cancel)
            if answer == mes.Ok:
                answer = mes.question(self, "Добавление " + file, "Вы точно отсканировали?", mes.Ok | mes.Cancel)
                if answer == mes.Ok:
                    pdf_merger = PyPDF2.PdfFileMerger()
                    files = os.listdir(folder)
                    path_to = self.path + "/документы/Договор/" + file + ".pdf"
                    for doc in files:
                        if ".pdf" in doc:
                            pdf_merger.append(str(folder + "/" + doc))
                    pdf_merger.write(path_to)
                    pdf_merger.close()
                    for doc in files:
                        os.remove(str(folder + "/" + doc))

    def create_journal(self):
        answer = mes.question(self, "Создание журнала работ", "Создать журнал работ?", mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            wnd = Journal(self)
            wnd.exec_()
        else:
            return

    def create_acts(self):
        answer = mes.question(self, "Создание Исполнительной", "Создать исполнительную?", mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            wnd = CreateReport(self)
            wnd.exec_()
        else:
            return

    def check_input(self):
        if "" in list([self.name.text(), self.number.text(),
                       self.my_object.toPlainText(), self.work.toPlainText(),
                      self.part.text(), self.price.text(), self.date_end.text()]) or self.date.text() == _zero:
            return msg(self, "Заполните все поля")
        if yong_date(young=self.date.text(), old=self.date_end.text()):
            return msg(self, "Дата начала старше даты окончания договора")
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True

    def start_menu(self):
        wnd = MenuContract(self, self.path)
        wnd.exec_()


designer_file_menu = get_path_ui("menu_contract")


class MenuContract(QDialog):
    def __init__(self, parent=None, path=None):
        super(MenuContract, self).__init__()
        uic.loadUi(designer_file_menu, self)
        self.parent = parent
        self.b_act.clicked.connect(self.open_file)
        self.b_journal.clicked.connect(self.open_file)
        self.b_def.clicked.connect(self.open_file)
        self.b_ekr.clicked.connect(self.open_file)
        self.b_mat.clicked.connect(self.open_file)
        self.b_contract.clicked.connect(self.open_file)
        self.b_act.setEnabled(False)
        self.b_journal.setEnabled(False)
        self.b_def.setEnabled(False)
        self.b_ekr.setEnabled(False)
        self.b_mat.setEnabled(False)
        self.b_contract.setEnabled(False)
        self.path = path
        self.check_files()

    def check_files(self):
        files = os.listdir(self.path)
        if "Документы" in files:
            files = os.listdir(self.path + "/Документы")
            if "Журнал работ.docx" in files:
                self.b_journal.setEnabled(True)
            if "Исполнительная.xlsx" in files:
                self.b_act.setEnabled(True)
            if "Договор" in files:
                files = os.listdir(self.path + "/Документы/Договор")
                if "ЕКР.pdf" in files:
                    self.b_ekr.setEnabled(True)
                if "Дефектная.pdf" in files:
                    self.b_def.setEnabled(True)
                if "Материалы.pdf" in files:
                    self.b_mat.setEnabled(True)
                if "Договор.pdf" in files:
                    self.b_contract.setEnabled(True)

    def open_file(self):
        text = self.sender().text()
        files = {"ЕКР": "/Документы/ЕКР.pdf",
                 "Дефектная": "/Документы/Дефектная.pdf",
                 "Договор": "/Документы/Договор.pdf",
                 "Журнал": "/Журнал работ.docx",
                 "Материалы": "/Документы/Материалы.pdf"}
        os.startfile(self.path + files[text])