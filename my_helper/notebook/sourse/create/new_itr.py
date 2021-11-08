from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
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
        self.list_ui = [self.family, self.name, self.surname, self.post,
                        self.passport, self.passport_date, self.passport_got,
                        self.adr, self.live_adr, self.cb_auto,
                        self.inn, self.snils,
                        self.n_td, self.d_td,
                        self.n_OT_p, self.d_OT, self.n_OT_c,
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