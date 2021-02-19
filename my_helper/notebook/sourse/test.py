from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.data = ""

    def initUI(self):
        self.setWindowTitle("title")
        self.setGeometry(300, 300, 600, 600)

        button = QtWidgets.QPushButton('push', self)
        button.setToolTip('This is an example button')
        button.move(100, 70)
        button.clicked.connect(self.on_click)
        self.show()

    def set_data(self, text):
        self.data = text

    @QtCore.pyqtSlot()
    def on_click(self):
        my_dialog = MyDialog(self)
        my_dialog.exec_()
        print(self.data)


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("title")
        self.setGeometry(300, 300, 500, 500)

        button = QtWidgets.QPushButton('dialog push', self)
        button.setToolTip('This is an example button')
        button.move(100, 70)
        button.clicked.connect(self.browserFile)
        self.show()

    @QtCore.pyqtSlot()
    def browserFile(self):
        self.close()

    def get_assignment(self):
        return {"name": "assignmentName", "due": "assignmentDue", "description": "description"}

    def close(self):
        self.parent.set_data("ghbdtn")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
