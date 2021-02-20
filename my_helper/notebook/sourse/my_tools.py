import os, sys
from PyQt5.QtWidgets import QMessageBox, QPushButton, QApplication
from PyQt5 import QtWidgets
from PyQt5 import uic
import config as conf


def calc_tap_segments():
    d = int(input("Введите диаметр голой трубы"))
    b = int(input("Введите толщину изоляции"))
    neck = int(input("Введите размер шейки"))
    back = int(input("Введите размер затылка"))
    L = int(input("Введите длину окружности по металлу"))
    count = int(input("Введите число сегментов"))
    my_count = count
    if back < 630:
        my_count = 5
    elif back < 1230:
        my_count = 7
    elif back < 2050:
        my_count = 9
    elif back < 3050:
        my_count = 11
    else:
        print("Слишком огромный отвод, сочувствую....")

    h = (back - neck) / (2 * my_count - 2)
    min_neck = neck / my_count
    max_back = min_neck + h
    radius = L / 6.28
    f = open("tmp.txt")
    f.write("высота h = " + str(h))
    f.write("шейка рыбки = " + str(min_neck))
    f.write("затылок рыбки = " + str(max_back))
    f.write("Радиус окружности = " + str(radius))
    f.close()
    os.startfile("tmp.txt", "print")
    os.remove("tmp.txt")
    return


class Notepad(QtWidgets):
    def __init__(self, parent=None):
        super(Notepad, self).__init__(parent)
        self.btn.clicked.connect(self.ev_close)
        self.text = self.get_text()
        self.file_note = conf.path + "/notepad.txt"
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Notepad')
        self.btn = QPushButton('Закрыть', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 50)
        self.text_area = QtWidgets.QPlainTextEdit()
        self.text_area.resize(200, 100)
        self.show()

    def get_text(self):
        file = open(self.file_note, 'r')
        text = file.read()
        file.close()
        return text

    def set_text(self):
        text_ui = self.text_area.toPlainText()
        file = open(self.file_note, 'w')
        file.write(text_ui + '\n')
        file.close()

    def ev_close(self):
        answer = QMessageBox.question(self, 'Вертикаль', "Сохранить записи?",
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.set_text()
            self.close()
        elif answer == QMessageBox.No:
            self.close()
        elif answer == QMessageBox.Cancel:
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Notepad()
    wnd.show()
    sys.exit(app.exec())