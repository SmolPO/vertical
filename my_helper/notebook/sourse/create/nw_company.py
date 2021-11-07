from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.create.new_template import TempForm
from my_helper.notebook.sourse.database import *
designer_file = get_path_ui("add_company")
fields = ["company", "adr", "ogrn", "inn", "kpp", "bik", "korbill", "rbill", "bank", "family", "name", "surname",
          "post", "count_attorney", "date_attorney", "id"]
statues_com = ["Заказчик", "Подрядчик", "Прочее"]


class NewCompany(TempForm):
    def __init__(self, parent=None):
        super(NewCompany, self).__init__(designer_file, parent, "company")
        if not self.status_:
            return
        self.init_mask()
        self.list_ui = [self.company, self.ogrn, self.inn, self.kpp, self.adr,
                        self.bik, self.korbill, self.rbill, self.bank,
                        self.big_boss, self.big_post, self.big_at, self.big_d_at,
                        self.mng_boss, self.mng_post, self.mng_at, self.mng_d_at,
                        self.cb_status]
        try:
            self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)
        except:
            msg(self, my_errors["2_get_path"])
            return

    def init_mask(self):
        self.ogrn.setValidator(QREVal(QRE("[0-9]{14}")))
        self.inn.setValidator(QREVal(QRE("[0-9]{10}")))
        self.kpp.setValidator(QREVal(QRE("[0-9]{9}")))
        self.bik.setValidator(QREVal(QRE("[0-9]{8}")))
        self.korbill.setValidator(QREVal(QRE("[0-9]{20}")))
        self.rbill.setValidator(QREVal(QRE("[0-9]{20}")))
        self.bank.setValidator(QREVal(QRE("[А-Яа-я /- 0-9]{10}")))
        self.big_boss.setValidator(QREVal(QRE("[а-яА-Я ]{30}")))
        self.big_post.setValidator(QREVal(QRE("[а-яА-Я ]{30}")))
        self.big_at.setValidator(QREVal(QRE("[А-Яа-я /- 0-9]{10}")))
        self.mng_boss.setValidator(QREVal(QRE("[а-яА-Я ]{30}")))
        self.mng_post.setValidator(QREVal(QRE("[а-яА-Я ]{30}")))
        self.mng_at.setValidator(QREVal(QRE("[А-Яа-я /- 0-9]{10}")))

    def _select(self, text):
        return True