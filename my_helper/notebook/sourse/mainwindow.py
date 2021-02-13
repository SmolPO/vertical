from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('../designer_ui/main_menu.ui', self)
        # pass
        self.b_pass_week.clicked.connect(self.ev_pass_week)
        self.b_pass_month.clicked.connect(self.ev_pass_month)
        self.b_pass_auto.clicked.connect(self.ev_pass_auto)
        self.b_pass_recover.clicked.connect(self.ev_pass_recover)
        self.b_pass_unlock.clicked.connect(self.ev_pass_unlock)
        self.b_pass_issue.clicked.connect(self.ev_pass_issue)
        # create
        self.b_new_person.clicked.connect(self.ev_new_person)
        self.b_new_bill.clicked.connect(self.ev_new_bill)
        self.b_new_build.clicked.connect(self.ev_new_build)
        self.b_new_boss.clicked.connect(self.ev_new_boss)
        self.b_new_boss_post.clicked.connect(self.ev_new_boss_post)
        self.b_new_invoice.clicked.connect(self.ev_new_invoice)

        self.b_create_act.clicked.connect(self.ev_create_act)
        self.b_get_material.clicked.connect(self.ev_get_material)
        self.b_pdf_check.clicked.connect(self.ev_pdf_check)
        self.b_send_covid.clicked.connect(self.ev_send_covid)
        self.b_connect.clicked.connect(self.ev_connect)

        self.b_journal.clicked.connect(self.ev_journal)
        self.b_tabel.clicked.connect(self.ev_tabel)
        self.b_scan.clicked.connect(self.ev_scan)
        self.b_attorney.clicked.connect(self.ev_attorney)
        self.b_invoice.clicked.connect(self.ev_invoice)

    def ev_pass_week(self):
        print("pass week")

    def ev_pass_month(self):
        print("pass month")

    def ev_pass_auto(self):
        print("pass auto")

    def ev_pass_recover(self):
        print("pass rec")

    def ev_pass_issue(self):
        print("pass issue")

    def ev_pass_unlock(self):
        print("pass unlock")

    def ev_new_boss(self):

        print("new boss")

    def ev_new_bill(self):
        print("new bill")

    def ev_new_build(self):
        print("new build")

    def ev_new_person(self):
        print("new person")

    def ev_create_act(self):
        print("create act")

    def ev_get_material(self):
        print("get mat")

    def ev_pdf_check(self):
        print("pdf check")

    def ev_send_covid(self):
        print("send covid")

    def ev_connect(self):
        self.r_connect.setChecked(True)
        print("connect")

    def ev_new_invoice(self):
        print("create invoice")

    def ev_new_boss_post(self):
        print("new post of boss")

    def ev_journal(self):
        print("journal")

    def ev_tabel(self):
        print("tabel")

    def ev_scan(self):
        self.r_connect.setChecked(True)
        print("scan")

    def ev_attorney(self):
        self.r_connect.setChecked(True)
        print("attorney")

    def ev_invoice(self):
        self.r_connect.setChecked(True)
        print("invoice")