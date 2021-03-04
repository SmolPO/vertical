from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class AddWorker(QDialog):
    def __init__(self, parent=None):
        super(AddWorker, self).__init__(parent)
        uic.loadUi('../designer_ui/add_worker.ui', self)
        # pass
        self.parent = parent
        self.b_OK.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.worker = list()

    def ev_OK(self):
        # считать все данные из формы
        self.worker.append([x.text() for x in [self.family, self.name, self.surname, self.position]])
        self.worker.append([x.text() for x in [self.series, self.number]])
        self.worker.append([x.toPlainText() for x in [self.passport_post, self.adr]])
        self.worker.append([x.text() for x in [self.ES, self.ES_group, self.d_ES]])
        self.worker.append([x.text() for x in [self.H_, self.H_group, self.d_H]])
        self.worker.append([x.text() for x in [self.OT, self.d_OT]])
        self.worker.append([x.text() for x in [self.PTM, self.d_PTM]])
        self.worker.append([x.text() for x in [self.study, self.contract, self.d_work]])
        print(self.worker)
        self.parent.get_new_worker(self.worker)
        print("OK")
        self.close()

    def ev_cancel(self):
        self.parent.get_new_worker(["not"])
        print("cancel")
        self.close()
