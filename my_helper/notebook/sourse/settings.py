from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QFileDialog
from configparser import ConfigParser


class Settings(QDialog):
    def __init__(self, parent=None):
        super(Settings, self).__init__()
        uic.loadUi('../designer_ui/settings.ui', self)
        self.parent = parent
        # pass
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_explorer.clicked.connect(self.ev_explorer)
        self.init_data()

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
        self.path.setText(config.get('path', 'path'))
        self.ip.setText(config.get('database', 'ip'))
        self.name_db.setText(config.get('database', 'name_db'))
        self.user_db.setText(config.get('database', 'user_db'))
        self.password_db.setText(config.get('database', 'password_db'))
        self.new_year.setValue(int(config.get('config', 'new_year')))

    def save_data(self, data):
        config = ConfigParser()
        config.read('config.ini')
        config.set('path', 'path', str(data[0]))
        config.set('database', 'ip', data[1])
        config.set('database', 'name_db', data[2])
        config.set('database', 'user_db', data[3])
        config.set('database', 'password_db', data[4])
        config.set('config', 'new_year', str(data[5]))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
