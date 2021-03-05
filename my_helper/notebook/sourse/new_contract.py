from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class NewContact(QDialog):
    def __init__(self, parent=None):
        super(NewContact, self).__init__(parent)
        uic.loadUi('../designer_ui/new_contract.ui', self)
        # pass
        self.parent = parent
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)

    def ev_OK(self):
        # считать все данные из формы
        print("OK")
        contract = list()
        contract.append([x.text() for x in [self.number, self.d_contract, self.name,
                                            self.company, self.ogrn, self.kpp, self.inn]])
        contract.append([x.toPlainText() for x in [self.obj, self.build, self.adr]])
        self.parent.create_new_contract(contract)
        self.close()

    def ev_cancel(self):
        print("cancel")
        self.close()
