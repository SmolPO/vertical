from pass_template import TempPass

#  сделать мессаджбоксы на Сохранить
designer_file = '../designer_ui/pass_unlock.ui'


class UnlockPass(TempPass):
    def __init__(self, parent):
        super(UnlockPass, self).__init__(designer_file, parent, "workers")
        # pass
        self.d_from.setDate(dt.datetime.now().date())
        self.d_to.setDate(dt.datetime.now().date())
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.init_workers()
        self.data = {"number": "", "data": "", "customer": "", "company": "", "start_date": "", "end_date": "",
                     "post": "", "family": "", "name": "", "surname": "", "adr": ""}
        self.main_file = self.path + "/patterns/unlock.docx"
        self.print_file = self.path + "/to_print/"

    def init_workers(self):
        self.cb_worker.addItem("(нет)")
        for name in self.parent.db.get_data("family, name", self.table):
            self.cb_worker.addItem(" ".join((name[0], name[1][0])) + ".")

    def _get_data(self):
        family = self.cb_worker.currentText()
        for row in self.parent.db.get_data("family, name, surname, post, live_adr", self.table):
            if family[:-3] == row[0]:  # на форме фамилия в виде Фамилия И.
                self.data["family"] = row[0]
                self.data["name"] = row[1]
                self.data["surname"] = row[2]
                self.data["post"] = row[3]
                self.data["adr"] = row[4]
                self.data["start_date"] = self.d_from.text()
                self.data["end_date"] = self.d_to.text()

    def check_input(self):
        return True

    def _create_data(self, doc):
        return True