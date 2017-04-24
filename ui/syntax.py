from PyQt5.QtWidgets import QHBoxLayout, QWidget, QListWidget, QMenu, QAction, QFileDialog, QSplitter
from PyQt5.QtCore import Qt
from PyQt5 import QtSvg
from PyQt5.Qt import QByteArray


class SyntaxAnalysisWidget(QWidget):
    def __init__(self, parent=None):
        super(SyntaxAnalysisWidget, self).__init__(parent)

        self.__left_bar = None
        self.__svg_widget = None

        self.__data = None
        self.__svg_trees = []

        # Setup Ui
        self.__setup_ui()

    def load_data(self, data):
        self.__data = data

        for sentence in self.__data.keys():
            self.__left_bar.addItem(sentence)
            self.__svg_trees.append(self.__data[sentence])

    def __setup_ui(self):
        # left bar & stacked widget setup
        self.__left_bar = QListWidget(self)
        self.__svg_widget = QtSvg.QSvgWidget()

        self.__left_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__left_bar.customContextMenuRequested.connect(self.__show_context_menu)

        self.__left_bar.currentRowChanged.connect(self.__display)  # change widget on a __stacked_widget

        # layout setup
        hbox_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.__left_bar)
        splitter.addWidget(self.__svg_widget)
        hbox_layout.addWidget(splitter)
        self.setLayout(hbox_layout)

    def __show_context_menu(self, point):
        global_pos = self.__left_bar.mapToGlobal(point)

        menu = QMenu()

        menu.addAction("Сохранить как изображение")
        menu.triggered[QAction].connect(self.__process_context_menu)

        menu.exec(global_pos)

    def __process_context_menu(self, menu_item):
        if menu_item.text() == "Сохранить как изображение":

            filename = QFileDialog.getSaveFileName(None, 'Сохранить SVG-граф', "", "svg files (*.svg)")

            if len(filename[0]) > 4:

                with open(filename[0], 'w', encoding='utf-8') as f:
                    f.write(self.__svg_trees[self.__left_bar.currentRow()])

    def __display(self, i):

        byte_array = QByteArray()
        byte_array.append(self.__svg_trees[i])

        self.__svg_widget.load(byte_array)
