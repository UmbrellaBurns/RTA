from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsEllipseItem, QDialog, QPushButton, QVBoxLayout, QGraphicsRectItem, \
    QGraphicsTextItem, QMenu, QGraphicsLineItem, QGraphicsView, QGraphicsScene, QWidget, QApplication, QHBoxLayout, \
    QInputDialog
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import QSize, QSizeF, QRect
from PyQt5.QtGui import QPainter
from semantical_analysis.block_item import Block, PortItem
from semantical_analysis.connection_item import Connection, ArrowItem, LabelItem
import math
import random


class GraphEditor(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMinimumSize(600, 400)

        random.seed(version=2)

        self.nodes = []

        self.connections = []

        # Widget layout and child widgets:
        self.horizontalLayout = QHBoxLayout(self)

        self.diagramScene = DiagramScene(self)
        self.diagramView = QGraphicsView(self.diagramScene, self)
        self.horizontalLayout.addWidget(self.diagramView)

        self.diagramView.setRenderHint(QtGui.QPainter.Antialiasing, on=True)

        self.started_connection = None

    def remove_connection(self, connection):
        self.diagramScene.removeItem(connection.arrow)
        self.diagramScene.removeItem(connection.arrow.text_label)

        self.connections.remove(connection)

    def start_connection(self, port):
        self.started_connection = Connection(port, None, self)

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def is_connection_exists(self, first_node, last_node):
        for connection in self.connections:
            if connection.get_first_node() == first_node and connection.get_last_node() == last_node:
                return True
        return False

    def load_diagram_from_graph(self, graph):
        # Read diagram from graph edges

        self.nodes = []
        self.connections = []

        self.diagramScene.clear()

        size = math.sqrt(len(graph.edges))

        x_shift = 100
        y_shift = 100
        i = 0

        for edge in graph.edges:
            first_node = edge.from_node.text
            last_node = edge.to_node.text
            link_type = edge.text

            # First Node
            i += 1
            x = x_shift * i
            y = y_shift
            f = self.add_node(x, y, first_node)

            if i > size:
                y_shift += 100
                i = 0

            # Last Node
            i += 1
            x = x_shift * i
            y = y_shift
            l = self.add_node(x, y, last_node)

            if i > size:
                y_shift += 100
                i = 0

            connection = Connection(f.get_random_port(), None, self)
            connection.set_link_type(link_type)
            connection.setToPort(l.get_random_port())

            self.connections.append(connection)

        # self.dump()

        # svg = QSvgGenerator()
        # svg.setFileName('graph.svg')
        # svg.setSize(QSize(self.diagramScene.width(), self.diagramScene.height()))
        # svg.setViewBox(QRect(0, 0, self.diagramScene.width(), self.diagramScene.height()))
        # svg.setTitle('Semantic Graph')
        # svg.setDescription('File created by RTA')

        # painter = QPainter()
        # painter.begin(svg)
        # self.diagramScene.render(painter)
        # painter.end()

        print('Triples loading is finished')

    def scene_mouse_move_event(self, event):
        if self.started_connection:
            pos = event.scenePos()
            self.started_connection.setEndPos(pos)

    def scene_mouse_release_event(self, event):
        if self.started_connection:
            pos = event.scenePos()
            items = self.diagramScene.items(pos)
            for item in items:
                if type(item) is PortItem:
                    if (not self.is_connection_exists(self.started_connection.fromPort.parent_block,
                                                      item.parent_block)) and (
                                self.started_connection.fromPort.parent_block is not item.parent_block):
                        self.started_connection.setToPort(item)

                        self.connections.append(self.started_connection)

            if self.started_connection.toPort is None:
                self.started_connection.delete()
            self.started_connection = None

    def add_node(self, x, y, text):
        node = Block(text, parent=self)
        node.setPos(x, y)
        self.diagramScene.addItem(node)
        self.nodes.append(node)
        return node

    def remove_node(self, node):

        delete_later = []

        for connection in self.connections:
            if connection.get_last_node() == node or connection.get_first_node() == node:
                delete_later.append(connection)

        for item in delete_later:
            self.remove_connection(item)

        self.diagramScene.removeItem(node)
        self.nodes.remove(node)

    def remove_selected_items(self):
        for item in self.diagramScene.selectedItems():
            if type(item) == Block:
                self.remove_node(item)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            self.add_block_item(self.diagramView.mapToScene(event.pos()))
            # self.dump()

    def add_block_item(self, pos):
        text, ok = QInputDialog.getText(None, 'Добавить элемент', 'Введите название:')
        if ok:
            self.add_node(pos.x(), pos.y(), str(text))

    def dump(self):

        print('||------- DUMP -------||')
        print('Nodes: ')

        for node in self.nodes:
            print(node.get_text())

        print('\nEdges: ')

        for connection in self.connections:
            first_node = connection.get_first_node().get_text()
            last_node = connection.get_last_node().get_text()
            link_type = connection.get_link_type()

            print('{0} {1} {2}'.format(first_node, link_type, last_node))

        print('||------- END --------||')

    def get_all_connections(self):
        return self.connections

    def get_all_nodes(self):
        return self.nodes

    def get_diagram_scene(self):
        return self.diagramScene

    def context_menu_event(self, event):
        menu = QMenu()
        add = menu.addAction('Добавить узел')
        add.triggered.connect(self.add_block_item)

        dump = menu.addAction('Dump')
        dump.triggered.connect(self.dump)

        menu.exec_(event.screenPos())


# DiagramScene - main scene


class DiagramScene(QGraphicsScene):
    def __init__(self, parent=None):
        self.parent = parent
        super(DiagramScene, self).__init__(parent)

    def mouseMoveEvent(self, mouse_event):
        self.parent.scene_mouse_move_event(mouse_event)
        super(DiagramScene, self).mouseMoveEvent(mouse_event)

    def mouseReleaseEvent(self, mouse_event):
        self.parent.scene_mouse_release_event(mouse_event)
        super(DiagramScene, self).mouseReleaseEvent(mouse_event)
