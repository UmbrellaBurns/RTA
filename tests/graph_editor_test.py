import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QAction, QMenu, QWidget, QFileDialog
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import QSize, QRect
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter, QPixmap, QImage
from semantical_analysis.graph_editor import GraphEditor
from ontology_processing.triples_to_owl import TriplesToOWL
from morphological_analysis.pymorphy_wrap import MorphAnalyzer
import random
import time


class SemanticAnalysisWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setMinimumSize(600, 400)

        random.seed(version=2)

        self.__graph_editor = GraphEditor()

        self.__morph = MorphAnalyzer()

        self.__btn_save = QPushButton("Экспорт..", self)

        self.__export_menu = QMenu()
        self.__action_to_owl = self.__export_menu.addAction("Web-онтология (owl-файл)")
        self.__action_to_svg = self.__export_menu.addAction("Файл векторной графики (svg-файл)")
        self.__action_to_cmap = self.__export_menu.addAction("Концептуальная карта (txt-файл)")
        self.__action_to_png = self.__export_menu.addAction("Изображение")

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
        elif menu_item.text() == "Изображение":
            self.export_to_png()

    def export_to_png(self):
        """
        Graph editor's scene rendering & saving to png-file
        """

        filename = QFileDialog.getSaveFileName(None, 'Сохранить в формате png', "", "Images (*.png)")

        if len(filename[0]) > 4:

            w = self.__graph_editor.get_diagram_scene().width()
            h = self.__graph_editor.get_diagram_scene().height()

            image = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
            image.fill(Qt.white)
            # pix = QPixmap(w, h)
            painter = QPainter()
            painter.begin(image)
            painter.setRenderHint(QPainter.Antialiasing)
            self.__graph_editor.get_diagram_scene().render(painter)
            painter.end()

            image.save(filename[0])

    def export_to_svg(self):
        """
        Graph editor's scene rendering & saving to svg-file
        :return: None
        """

        filename = QFileDialog.getSaveFileName(None, 'Сохранить SVG-граф', "", "svg files (*.svg)")

        if len(filename[0]) > 4:

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

        if len(filename[0]) > 4:
            out = ""

            processed_nodes = []

            for connection in self.__graph_editor.get_all_connections():
                first_node = connection.get_first_node().get_text()
                last_node = connection.get_last_node().get_text()
                link_type = connection.get_link_type()

                processed_nodes.append(first_node)
                processed_nodes.append(last_node)

                out += '{0}	{1}	{2}'.format(first_node, link_type, last_node) + '\n'

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

        filename = QFileDialog.getSaveFileName(None, 'Экспорт в OWL', "", "OWL files (*.owl)")

        time_stamp = time.time()

        if len(filename[0]) > 4:

            processed_nodes = []

            triples = []

            for connection in self.__graph_editor.get_all_connections():
                first_node = connection.get_first_node().get_text()
                second_node = connection.get_last_node().get_text()
                link_type = connection.get_link_type()

                # pos tagging

                first_node_pos = [item.tag.POS for item in self.__morph.parse(first_node)]
                second_node_pos = [item.tag.POS for item in self.__morph.parse(second_node)]

                if 'NOUN' in first_node_pos and 'NOUN' in second_node_pos:
                    triples.append([first_node, link_type, second_node])

                    processed_nodes.append(first_node)
                    processed_nodes.append(second_node)

            for node in self.__graph_editor.get_all_nodes():
                if node.get_text() not in processed_nodes:
                    # pos tagging
                    node_pos = [item.tag.POS for item in self.__morph.parse(node.get_text())]

                    if 'NOUN' in node_pos:
                        processed_nodes.append(node.get_text())
                        triples.append([node.get_text()])

            owl_exporter = TriplesToOWL(triples)

            owl_exporter.processing()

            owl_exporter.to_file(filename[0])

        print("Finished: time - {}".format((time.time() - time_stamp)))

    def load_diagram_from_graph(self, graph):
        # Read diagram from graph edges

        self.__graph_editor.load_diagram_from_graph(graph)
