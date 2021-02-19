#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication)

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('open', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()

    def onActivated(self, text):
        items = ("Red", "Blue", "Green")
        item, okPressed = QInputDialog.getItem(self, "Get item", "Color:", items, 0, False)
        if okPressed and item:
            print(item)

class Example2(QInputDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('OK', self)
        self.btn.move(20, 20)
        self.le = QLineEdit(self)
        self.le.move(130, 22)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def getText(parent: QWidget, title: str, label: str):
        print(1)
        return (4, 8)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())