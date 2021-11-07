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
        self.cb_select.activated[str].connect(self.ev_select)
        try:
            self.parent.db.init_list(self.cb_select, "number, id", self.table)
            self.init_company()
        except:
            msg(self, my_errors["3_get_db"])
            return
        self.list_ui = [self.name, self.cb_comp, self.number, self.date, self.my_object, self.work, self.part,
                        self.price, self.date_end, self.nds, self.avans, self.status]

        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = len(self.list_ui)
        self.cb_comp.addItem(self.parent.customer)
        self.b_menu.setEnabled(False)

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я ]{30}"))
        self.name.setValidator(symbols)
        self.number.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.part.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.price.setValidator(QREVal(QRE("[,0-9]{1000}")))

    def _select(self, text):
        self.b_menu.setEnabled(False) if text == empty else self.b_menu.setEnabled(True)
        return True

    def init_company(self):
        self.companies = self.parent.db.get_data("*", "company")
        for item in self.companies:
            if item[-2] == "Заказчик":
                self.cb_comp.addItem(item[-1] + ". " + item[0])

    def _set_data(self, data):
        g = iter(range(len(self.rows_from_db) + 1))
        for i in range(10):
            self.cb_comp.setCurrentIndex(i)
            print(self.cb_comp.currentText() + ".")
        for item in self.companies:
            if data[1] == item[0]:
                my_id = self.get_id(data[1], 0, "company")
                ind = self.cb_comp.findText(my_id + ". " + data[1])
                self.cb_comp.setCurrentIndex(ind)
                break
        path_docs = get_path("path") + get_path("path_contracts")
        self.path = path_docs + "/" + self.number.text()

    def get_id(self, val, field, table):
        rows = self.parent.db.get_data("*", table)
        for item in rows:
            if item[field] == val:
                return item[-1]
        pass

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
        self.create_acts()
        self.create_doc()
        self.create_journal()

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