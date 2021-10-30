from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from my_helper.notebook.sourse.database import get_path_ui
designer_file = get_path_ui("contract")


class Contract(QDialog):
    pass