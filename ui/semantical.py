from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QGraphicsRectItem, \
    QAction, QMenu, QGraphicsView, QGraphicsScene, QWidget, QApplication, QHBoxLayout, \
    QFileDialog
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import QSize, QSizeF, QRect
from PyQt5.QtGui import QPainter
from semantical_analysis.graph_editor import GraphEditor

import random


class SemanticAnalysisWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setMinimumSize(600, 400)

        random.seed(version=2)

        self.__graph_editor = GraphEditor()

        self.__btn_save = QPushButton("Экспорт..", self)

        self.__export_menu = QMenu()
        self.__action_to_owl = self.__export_menu.addAction("Web-онтология (owl-файл)")
        self.__action_to_svg = self.__export_menu.addAction("Файл векторной графики (svg-файл)")
        self.__action_to_cmap = self.__export_menu.addAction("Концептуальная карта (txt-файл)")

        self.__btn_save.setMenu(self.__export_menu)

        self.__export_menu.triggered[QAction].connect(self.__process_export_menu)

        self.__setup_ui()

    def __setup_ui(self):

        vbox_layout = QVBoxLayout()

        self.__btn_save.setMaximumWidth(100)

        vbox_layout.addWidget(self.__btn_save)

        vbox_layout.addWidget(self.__graph_editor)

        self.setLayout(vbox_layout)

    def __process_export_menu(self, menu_item):

        if menu_item.text() == "Web-онтология (owl-файл)":
            self.export_to_owl()
        elif menu_item.text() == "Файл векторной графики (svg-файл)":
            self.export_to_svg()
        elif menu_item.text() == "Концептуальная карта (txt-файл)":
            self.export_to_cmap()

    def export_to_svg(self):
        """
        Graph editor's scene rendering & saving to svg-file
        :return: None
        """

        filename = QFileDialog.getSaveFileName(None, 'Сохранить SVG-граф', "", "svg files (*.svg)")

        if len(filename[0]) <= 0:
            filename = 'graph.svg'

        svg = QSvgGenerator()
        svg.setFileName(filename[0])

        w = self.__graph_editor.get_diagram_scene().width()
        h = self.__graph_editor.get_diagram_scene().height()

        svg.setSize(QSize(w, h))
        svg.setViewBox(QRect(0, 0, w, h))
        svg.setTitle('Semantic Graph')
        svg.setDescription('File created by RTA')

        painter = QPainter()
        painter.begin(svg)
        self.__graph_editor.get_diagram_scene().render(painter)
        painter.end()

    def export_to_cmap(self):
        """
        Graph editor's relations saving to txt-file
        :return: None
        """

        filename = QFileDialog.getSaveFileName(None, 'Экспорт в CMap', "", "Text files (*.txt)")

        if len(filename[0]) <= 0:
            filename = 'graph.txt'

        out = ""

        processed_nodes = []

        for connection in self.__graph_editor.get_all_connections():
            first_node = connection.get_first_node().get_text()
            last_node = connection.get_last_node().get_text()
            link_type = connection.get_link_type()

            processed_nodes.append(first_node)
            processed_nodes.append(last_node)

            out += '{0}  {1}  {2}'.format(first_node, link_type, last_node) + '\n'

        for node in self.__graph_editor.get_all_nodes():
            if node.get_text() not in processed_nodes:
                processed_nodes.append(node.get_text())

                out += node.get_text() + '\n'

        with open(filename[0], 'w', encoding='utf-8') as f:
            f.write(out)

    def export_to_owl(self):
        """
        Graph editor's relations export to owl-file
        :return: None
        """

        processed_nodes = []

        triples = []

        for connection in self.__graph_editor.get_all_connections():
            first_node = connection.get_first_node().get_text()
            last_node = connection.get_last_node().get_text()
            link_type = connection.get_link_type()

            triples.append([first_node, link_type, last_node])

            processed_nodes.append(first_node)
            processed_nodes.append(last_node)

            triples.append([first_node, link_type, last_node])

        for node in self.__graph_editor.get_all_nodes():
            if node.get_text() not in processed_nodes:
                processed_nodes.append(node.get_text())

                triples.append([node.get_text(), None, None])

        owl_exporter = None
        # TODO: OWL-processing
        # TODO: node text validation (ignore prepositions, conjunctions, etc.)

    def load_diagram_from_graph(self, graph):
        # Read diagram from graph edges

        self.__graph_editor.load_diagram_from_graph(graph)
