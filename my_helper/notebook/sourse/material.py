from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QVBoxLayout, QGroupBox, QApplication, QMainWindow, QLabel
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect


class Materiall(QMainWindow):
    def __init__(self):
        super(Materiall, self).__init__()
        # pass

        grid = QGridLayout()
        grid.setSpacing(10)
        self.btn = QPushButton(self)
        grid.addWidget(self.btn, 1, 1)
        grid.addWidget(self.btn, 1, 3)
        grid.addWidget(self.btn, 1, 4)
        grid.addWidget(self.btn, 2, 1, 4, 4)
        self.setLayout(grid)


if __name__ == "__main__":
    # app = Notebook()
    app = QApplication(sys.argv)
    ex = Materiall()
    ex.show()
    sys.exit(app.exec())
