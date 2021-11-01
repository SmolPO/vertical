from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import openpyxl as xlxs
from openpyxl.styles import Border
import datetime as dt
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.database import get_path_ui, get_path, get_config
designer_file = get_path_ui("create_report")
idx_table = 25


class CreateReport(QDialog):
    def __init__(self, parent):
        super(CreateReport, self).__init__()
        if not self.check_start():
            return
        self.parent = parent
        self.b_ok.clicked.connect(self.ev_ok)
        self.count_p2 = 0
        self.count_p5 = 0
        self.path = get_path("path_pat_patterns") + "/report.docx"
        self.data = dict()
        self.init_bosses()
        self.list_ui = [[self.act_1, self.act_2, self.act_3, self.act_4, self.act_5,
                         self.act_6, self.act_7, self.act_8, self.act_9, self.act_10],
                        [self.mat_1, self.mat_2, self.mat_3, self.mat_4],
                        [self.cult_1, self.cult_2, self.cult_3, self.cult_4],
                        [self.tabel_1, self.tabel_2],
                        [self.stor_1, self.stor_2, self.stor_3, self.stor_4]]
        self.init_bosses()
        self.init_contract()

    def check_start(self):
        self.status_ = True
        self.path_ = designer_file
        try:
            uic.loadUi(designer_file, self)
            return True
        except:
            mes.question(self, "Сообщение", "Не удалось открыть форму " + designer_file, mes.Cancel)
            self.status_ = False
            return False

    def init_bosses(self):
        for item in self.list_ui:
            for ui in item:
                self.parent.parent.db.init_list(ui, "id, family, name, surname", "itrs", people=True)
                self.parent.parent.db.init_list(ui, "id, family, name, surname", "bosses", people=True)
        pass

    def init_contract(self):
        self.parent.parent.db.init_list(self.contract, "id, family, name, surname", "itrs", people=True)
        pass

    def get_data(self):
        data = dict()
        return data

    def get_post(self, my_id, table):
        rows = self.parent.parent.db.get_data("*", table)
        for item in rows:
            if str(item[-1]) == my_id:
                print(item)
                return item[3]
        return "."

    def ev_ok(self):
        doc = xlxs.open("/covid.xlsx")
        contract = self.parent.parent.db.get_data("*",  "contract")
        company = self.parent.parent.db.get_data("*",  "company")
        print(company[0])
        print(contract[0])
        sheet = doc["result"]
        """
        Ввести данные из запроса по номеру контракта и компании
        """

        sheet.cell(row=2, column=1).value = 0
        file_path = "/covid/" + str(dt.datetime.now().date()) + "_" + self.parent.company
        doc.save(file_path)
        self.close()

    def create_ekr(self, data, sheet):
        """
        1;3;7
        :param data:
        :return:
        """
        parts = data.split(";")  # 5;5;8
        for item in parts:
            sheet.insert_rows(idx=idx_table, amount=5*item)
            cells = sheet['A'+str(idx_table):'F'+5*item]
            for cell in cells:
                cell.style.borders.left.border_style = Border.BORDER_THIN
                if int(cells.coordinate[1:])-idx_table/5 == 0:
                    cell.value = "работа"

            sheet.insert_rows(idx=idx_table)
            sheet.merge_cells(start_row=idx_table, start_column=1, end_row=idx_table, end_column=6)
            sheet.cell(row=idx_table, colomn=1).style.borders.left.border_style = Border.BORDER_THICK
        pass

    def check_input(self):
         return True