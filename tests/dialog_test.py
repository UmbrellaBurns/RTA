import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
    QLabel, QApplication)
from utils.category_dialog import CategoryDialog


def dialog_testing():
        app = QApplication(sys.argv)

        cd = CategoryDialog()

        cd.exec_()

        res = cd.value()

        t = 5

        sys.exit(app.exec_())