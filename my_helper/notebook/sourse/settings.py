from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog
from configparser import ConfigParser
from database import get_path_ui, my_errors
from PyQt5.QtWidgets import QMessageBox as mes
designer_file = get_path_ui("settings")


class Settings(QDialog):
    def __init__(self, parent=None):
        super(Settings, self).__init__()
        if not self.check_start():
            return
        uic.loadUi(designer_file, self)
        self.parent = parent
        # my_pass
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_explorer.clicked.connect(self.ev_explorer)
        self.init_data()

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

    def ev_OK(self):
        data = self.get_data()
        self.save_data(data)
        self.close()
        pass

    def ev_cancel(self):
        self.close()

    def ev_explorer(self):
        self.filename, tmp = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         "C:/", "*.*")
        self.path.setText(self.filename)

    def get_data(self):
        data = list()
        data.append(self.path.text())
        data.append(self.ip.text())
        data.append(self.name_db.text())
        data.append(self.user_db.text())
        data.append(self.password_db.text())
        data.append(str(self.new_year.value()))
        return data

    def init_data(self):
        config = ConfigParser()
        config.read('config.ini')
        try:
            self.path.setText(config.get('path', 'path'))
            self.ip.setText(config.get('database', 'ip'))
            self.name_db.setText(config.get('database', 'name_db'))
            self.user_db.setText(config.get('database', 'user_db'))
            self.password_db.setText(config.get('database', 'password_db'))
            self.new_year.setValue(int(config.get('config', 'new_year')))
        except:
            mes.question(self, "Сообщение", my_errors["8_get_data"], mes.Cancel)
            return False

    def save_data(self, data):
        config = ConfigParser()
        try:
            config.read('config.ini')
            config.set('path', 'path', str(data[0]))
            config.set('database', 'ip', data[1])
            config.set('database', 'name_db', data[2])
            config.set('database', 'user_db', data[3])
            config.set('database', 'password_db', data[4])
            config.set('config', 'new_year', str(data[5]))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        except:
            mes.question(self, "Сообщение", my_errors["8_get_data"], mes.Cancel)
            return False

