from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from add_company import AddCompany
from new_boss import NewBoss

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

        self.get_param_from_widget = None

    def ev_pass_week(self):
        # открыть диалоговое окно дл выбора дней. Открыть календарь.
        # получить из БД список сотрудников, дата рождения, паспортные, место жительства
        # сформировать документ
        # направить на печать
        print("pass week")

    def ev_pass_month(self):
        # получить из БД список сотрудников, дата рождения, паспортные, место жительства
        # сформировать документ
        # направить на печать
        print("pass month")

    def ev_pass_auto(self):
        # получить из БД список машин, номер, владельцы
        # сформировать документ
        # направить на печать
        print("pass auto")

    def ev_pass_recover(self):
        # получить список работников
        # открыть диалоговое окно с выбором сотрудника
        # cформировать документ
        # отправить на печать
        print("pass rec")

    def ev_pass_issue(self):
        # диалоговое окно с вводом нового сотрудника
        # ввод данных
        # добавление в БД
        print("pass issue")

    def ev_pass_unlock(self):
        # получить список работников
        # открыть диалоговое окно с выбором сотрудника
        # cформировать документ
        # отправить на печать
        print("pass unlock")

    def ev_new_boss(self):
        # диалоговое окно с формой для нового босса
        # заполнение данных
        # добавление в БД
        wnd = NewBoss()
        wnd.show()
        print("new boss")

    def ev_new_bill(self):
        # открыть сканер
        # распознать отсканированный
        # добавить значение в БД
        # сохранить скрин в папку месяца
        print("new bill")

    def ev_new_build(self):
        # открыть форму для нового объекта
        # заполнить данные
        # добавить объект в БД
        # получить новый список объектов для списка объектов на главном меню
        print("new build")

    def ev_new_person(self):
        # открыть окно для нового сотрудника
        # заполнить данные
        # отправить в БД
        print("new person")

    def ev_create_act(self):
        print("create act")

    def ev_get_material(self):
        # открыть форму для ввода название материала и даты завоза
        # сформировать документ
        # печать
        print("get mat")

    def ev_pdf_check(self):
        # открыть директорию
        # рассортировать все отсканированные файлы по папкам
        print("pdf check")

    def ev_send_covid(self):
        # если нет соответствующего файла, то открыть окно для сканирования
        # сформировать письмо
        # взять ковид из папки
        # отправить
        print("send covid")

    def ev_connect(self):
        # подключиться к серверу
        self.r_connect.setChecked(True)
        print("connect")

    def ev_new_invoice(self):
        # открыть сканер
        # добавить накладную в папку
        print("create invoice")

    def ev_new_boss_post(self):
        # получить весь список боссов
        # открыть окно для нового босса. Боса можно выбрать старого или ввести новые данные.
        # ввести данные
        # добавить в БД
        print("new post of boss")

    def ev_journal(self):
        # печать ковид журнала
        print("journal")

    def ev_tabel(self):
        # печать табеля
        print("tabel")

    def ev_scan(self):
        # открыть сканер
        print("scan")

    def ev_attorney(self):
        # печать доверенности
        self.r_connect.setChecked(True)
        print("attorney")

    def ev_invoice(self):
        # печать накладной
        self.r_connect.setChecked(True)
        print("invoice")


if __name__ == "__main__":
    # app = Notebook()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
