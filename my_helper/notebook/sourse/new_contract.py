from PyQt5.QtCore import QRegExp as QRE
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QRegExpValidator as QREVal
import os
import PyPDF2
from new_template import TempForm
from database import *
from journal import Journal
from report import CreateReport
statues_cntr = ["Начат", "Завершен"]


class NewContact(TempForm):
    def __init__(self, parent=None):
        self.status_ = True
        self.conf = Ini(self)
        ui_file = self.conf.get_path_ui("new_contract")
        if not ui_file:
            self.status_ = False
            return
        super(NewContact, self).__init__(ui_file, parent, "contracts")
        if not self.status_:
            return
        self.init_mask()
        self.b_docs.clicked.connect(self.create_docs)
        self.b_menu.clicked.connect(self.start_menu)
        self.cb_select.activated[str].connect(self.ev_select)
        if self.parent.db.init_list(self.cb_select, "number, id", self.table) == ERR:
            self.status_ = False
            return
        self.list_ui = [self.name, self.cb_comp, self.number, self.date, self.my_object, self.work,
                        self.part, self.price, self.date_end, self.nds, self.avans, self.status]
        self.cb_comp.addItem(self.parent.customer)
        self.b_menu.setEnabled(False)
        path_1 = self.conf.get_path("path")
        path_2 = self.conf.get_path("path_contracts")
        if path_1 == ERR or path_2 == ERR:
            self.status_ = False
            return
        self.path = path_1 + path_2

    def init_mask(self):
        self.price.setValidator(QREVal(QRE("[,0-9]{1000}")))

    def _select(self, text):
        self.b_menu.setEnabled(False) if text == empty else self.b_menu.setEnabled(True)
        return True

    def create_docs(self):
        if not self.check_input():
            return
        contract = str(self.number.text())
        folders = self.check_folder(contract, self.path)
        if folders == ERR:
            return ERR
        self.path += "/" + contract
        if folders:
            for item in folders:
                try:
                    os.mkdir(self.path + item)
                except:
                    return msg_er(self, CREATE_FOLDER)

        if self.create_acts():
            msg_info(self, CREATE_ACT)
        if self.create_doc() == ERR:
            msg_info(self, CREATE_DOCS)
        if self.create_journal():
            msg_info(self, CREATE_JOURNAL)

    def check_folder(self, contract, path):
        path_docs = path + "/" + contract
        _folders = ["", "/Документы", "/Документы/ППР", "/Документы/Договор", "/Документы/Приложение",
                    "/Документы/Приложение/Фото", "/Документы/Приложение/Накладные"]
        folders = []
        current_folder = s_list_dir(self, path)
        if current_folder == ERR:
            return ERR
        if not contract in current_folder:
            return _folders
        else:
            current_folder = s_list_dir(self, path_docs)
            if current_folder == ERR:
                return ERR

            if not "Документы" in current_folder:
                return _folders[1:]

            current_folder = s_list_dir(self, path_docs + "/Документы")
            if current_folder == ERR:
                return ERR

            if not "ППР" in current_folder:
                folders.append(_folders[2])
            if not "Договор" in current_folder:
                folders.append(_folders[3])
            if not "Приложение" in current_folder:
                return _folders[4:]
            else:

                current_folder = s_list_dir(self, path_docs + "/Документы/Приложение")
                if current_folder == ERR:
                    return ERR

                if not "Фото" in current_folder:
                    folders.append(_folders[5])
                if not "Накладные" in current_folder:
                    folders.append(_folders[6])

    def create_doc(self):
        path_1 = self.conf.get_path("path")
        path_2 = self.conf.get_path("path_scan")
        if path_1 == ERR or path_2 == ERR:
            return ERR
        folder = path_1 + path_2
        types = ["Договор", "ЕКР", "Дефектная", "Материалы"]
        for file in types:
            answer = msg_q(self,  "Отсканируйте " + file + " в PDF по порядку и затем нажмите ОК.")
            if answer == mes.Ok:
                answer = msg_q(self, "Вы точно отсканировали?")
                if answer == mes.Ok:
                    pdf_merger = PyPDF2.PdfFileMerger()
                    files = s_list_dir(folder)
                    if files == ERR:
                        return ERR
                    path_to = self.path + "/документы/Договор/" + file + ".pdf"
                    for doc in files:
                        if ".pdf" in doc:
                            try:
                                pdf_merger.append(str(folder + "/" + doc))
                            except:
                                return msg_er(self, GET_FILE + str(folder + "/" + doc))
                    try:
                        pdf_merger.write(path_to)
                    except:
                        return msg_er(self, GET_FILE + path_to)
                    pdf_merger.close()
                    for doc in files:
                        try:
                            os.remove(str(folder + "/" + doc))
                        except:
                            return msg_er(self, GET_FILE + str(folder + "/" + doc))

    def create_journal(self):
        answer = msg_q(self, "Создать журнал работ?")
        if answer == mes.Ok:
            wnd = Journal(self)
            if not wnd.status_:
                return ERR
            wnd.exec_()

    def create_acts(self):
        answer = msg_q(self, "Создать исполнительную?")
        if answer == mes.Ok:
            wnd = CreateReport(self)
            if not wnd.status_:
                return ERR
            wnd.exec_()
        else:
            return

    def check_input(self):
        if "" in list([self.name.text(), self.number.text(),
                       self.my_object.toPlainText(), self.work.toPlainText(),
                      self.part.text(), self.price.text(), self.date_end.text()]) or self.date.text() == ZERO:
            msg_info(self, FULL_ALL)
            return False
        if yong_date(young=self.date.text(), old=self.date_end.text()):
            msg_info(self, WRONG_DATE)
            return False
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True

    def start_menu(self):
        wnd = MenuContract(self, self.path)
        if not wnd.status_:
            return ERR
        wnd.exec_()


class MenuContract(QDialog):
    def __init__(self, parent=None, path=None):
        self.status_ = True
        self.conf = Ini(self)
        ui_file = self.conf.get_path_ui("menu_contract")
        if not ui_file:
            self.status_ = False
            return
        super(MenuContract, self).__init__()
        uic.loadUi(ui_file, self)
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
        files = s_list_dir(self, self.path)
        if files == ERR:
            return

        if "Документы" in files:
            files = s_list_dir(self, self.path + "/Документы")
            if files == ERR:
                return

            if "Журнал работ.docx" in files:
                self.b_journal.setEnabled(True)
            if "Исполнительная.xlsx" in files:
                self.b_act.setEnabled(True)
            if "Договор" in files:

                files = s_list_dir(self, self.path + "/Документы/Договор")
                if files == ERR:
                    return

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
        try:
            os.startfile(self.path + files[text])
        except:
            return msg_er(self, GET_FILE + self.path + files[text])


def s_list_dir(self, path):
    try:
        return os.listdir(path)
    except:
        return msg_er(self, GET_FILE + path)
