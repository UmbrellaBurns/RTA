from PyQt5.QtWidgets import QDialog, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem
from PyQt5.QtCore import QObject


class CategoryDialog(QDialog):
    def __init__(self, parent=None):
        super(CategoryDialog, self).__init__(parent)

        self.__combo = QComboBox()

        self.__btn_accept = QPushButton("Принять")
        self.__btn_cancel = QPushButton("Отмена")

        self.__value = None

        self.__setup_ui()

    def __setup_ui(self):
        self.__combo.addItems(
            ['ПОЛИТИКА', 'КУЛЬТУРА', 'СПОРТ', 'ЗДОРОВЬЕ', 'ТЕХНОЛОГИИ', 'ЭКОНОМИКА', 'ИНЦИДЕНТ', 'ТРАНСПОРТ', 'ЖЕНЩИНЫ',
             'РЕКЛАМА', 'СОЦИАЛЬНАЯ СФЕРА', 'НЕДВИЖИМОСТЬ', 'НАУКА'])

        self.__btn_accept.clicked.connect(self.__accept)
        self.__btn_cancel.clicked.connect(self.__cancel)

        # setup layout

        vbox_layout = QVBoxLayout()

        vbox_layout.addWidget(self.__combo)

        hbox_layout = QHBoxLayout()

        hbox_layout.addWidget(self.__btn_accept)
        hbox_layout.addWidget(self.__btn_cancel)
        vbox_layout.addLayout(hbox_layout)

        self.setLayout(vbox_layout)

    def value(self):
        return self.__value

    def __accept(self):
        self.__value = self.__combo.currentText()
        self.accept()

    def __cancel(self):
        self.close()
        return None
