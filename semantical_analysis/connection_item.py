from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsEllipseItem, QDialog, QPushButton, QVBoxLayout, QGraphicsRectItem, \
    QGraphicsTextItem, QMenu, QGraphicsLineItem, QGraphicsView, QGraphicsScene, QWidget, QApplication, \
    QHBoxLayout, QListView, QInputDialog
from math import acos, sin, cos, pi


class Connection:
    def __init__(self, fromPort, toPort, parent):

        self.parent = parent

        self.fromPort = fromPort
        self.pos1 = None
        self.pos2 = None
        if fromPort:
            self.pos1 = fromPort.scenePos()
            self.pos2 = fromPort.scenePos()
            fromPort.posCallbacks.append(self.setBeginPos)
            # custom
            self.arrow = ArrowItem(self, self.parent)
            self.setBeginPos(fromPort.scenePos())
        self.toPort = toPort
        # Create arrow item:

        self.parent.diagramScene.addItem(self.arrow)

    def get_first_node(self):
        return self.fromPort.parent_block

    def get_last_node(self):
        return self.toPort.parent_block

    def get_link_type(self):
        return self.arrow.get_text()

    def get_arrow(self):
        return self.arrow

    def set_link_type(self, type):
        self.arrow.set_text(type)

    def remove_connection(self):
        self.parent.diagramScene.removeItem(self.arrow)

    def setFromPort(self, fromPort):
        self.fromPort = fromPort
        if self.fromPort:
            self.pos1 = fromPort.scenePos()
            self.fromPort.posCallbacks.append(self.setBeginPos)

    def setToPort(self, toPort):
        self.toPort = toPort
        if self.toPort:
            self.pos2 = toPort.scenePos()
            self.toPort.posCallbacks.append(self.setEndPos)
            # custom
            self.setEndPos(toPort.scenePos())

            center = 0.5 * self.arrow.line().p1() + 0.5 * self.arrow.line().p2()
            x = center.x()
            y = center.y()
            self.arrow.text_label.setPos(x, y)
            self.arrow.text_appeared = True
            if self.arrow.get_text() == '':
                self.arrow.text_label.edit_parameters()
            self.parent.diagramScene.addItem(self.arrow.text_label)

    def setEndPos(self, endpos):
        self.pos2 = endpos
        self.arrow.setLine(QLineF(self.pos1, self.pos2))

    def setBeginPos(self, pos1):
        self.pos1 = pos1
        self.arrow.setLine(QLineF(self.pos1, self.pos2))

    def delete(self):
        self.parent.diagramScene.removeItem(self.arrow)
        # Remove position update callbacks:


class LabelItem(QGraphicsRectItem):
    def __init__(self, text='', parent=None):
        super(LabelItem, self).__init__(None)

        self.parent = parent
        self.text = text

        # Properties of the rectangle:
        self.setPen(QtGui.QPen(QtCore.Qt.lightGray))
        self.setBrush(QtGui.QBrush(QColor(234, 193, 72)))
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        # Label:
        self.label = QGraphicsTextItem(self.text, self)

        metric = QFontMetrics(self.label.font())
        self.width = metric.width(self.text)
        self.height = metric.height()

        self.setRect(0.0, 0.0, self.width + 1, self.height + 1)

    def contextMenuEvent(self, event):
        menu = QMenu()

        pa = menu.addAction('Параметры')
        pa.triggered.connect(self.edit_parameters)

        drop = menu.addAction('Удалить связь')
        drop.triggered.connect(self.remove_connection)

        menu.exec_(event.screenPos())

    def remove_connection(self):
        self.parent.delete_connection()

    def set_text(self, text):
        self.parent.arrow_text = str(text)
        self.text = str(text)
        self.label.setPlainText(text)

        metric = QFontMetrics(self.label.font())
        width = metric.width(self.text)
        height = metric.height()

        if self.height < height + 5:
            self.height = height + 5
        if self.width < width + 5:
            self.width = width + 5
        self.setRect(0.0, 0.0, self.width, self.height)
        # center label:
        rect = self.label.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx = (self.width - lw) / 2
        ly = (self.height - lh) / 2
        self.label.setPos(lx + 1, ly)

    def edit_parameters(self):
        text, ok = QInputDialog.getText(None, 'Параметры', 'Отношение:', text=self.text)
        if ok:
            self.set_text(text)

    def change_size(self, w, h):
        """ Resize block function """
        # Limit the block size:
        metric = QFontMetrics(self.label.font())
        width = metric.width(self.text)
        height = metric.height()

        if h < height + 5:
            self.height += 5
        if w < width + 5:
            self.width += 5
        self.setRect(0.0, 0.0, self.width, self.height)
        # center label:
        rect = self.label.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx = (w - lw) / 2
        ly = (h - lh) / 2
        self.label.setPos(lx, ly)

        return w, h


class ArrowItem(QGraphicsLineItem):
    def __init__(self, connection, scene):
        super(ArrowItem, self).__init__(None)
        self.setPen(QtGui.QPen(QColor(174, 22, 15), 2))
        self.setFlag(self.ItemIsSelectable, True)

        self.parent = scene
        self.connection = connection

        self.arrow_head = QPolygonF()

        self.arrow_text = ""
        self.text_label = LabelItem("", self)
        self.text_appeared = False

    def get_text(self):
        return self.arrow_text

    def set_text(self, text):
        self.text_label.set_text(text)

    def contextMenuEvent(self, event):
        menu = QMenu()
        delete = menu.addAction('Delete')
        delete.triggered.connect(self.delete_connection)
        menu.exec_(event.screenPos())

    def delete_connection(self):
        self.parent.remove_connection(self.connection)

    def paint(self, QPainter, QStyleOptionGraphicsItem, widget=None):
        painter = QPainter

        painter.setPen(QtGui.QPen(QColor(174, 22, 15), 2))
        painter.setBrush(QColor(174, 22, 15))
        painter.drawLine(self.line())

        if self.text_appeared:
            center = 0.5 * self.line().p1() + 0.5 * self.line().p2()
            x = center.x() - self.text_label.width / 2
            y = center.y() - self.text_label.height / 2
            self.text_label.setPos(x, y)

            # Draw arrow head
            size = 10
            angle = acos(self.line().dx() / self.line().length())
            if self.line().dy() >= 0:
                angle = pi * 2 - angle

            arrow_p1 = self.line().p2() + QPointF(sin(angle - pi / 3) * size, cos(angle - pi / 3) * size)
            arrow_p2 = self.line().p2() + QPointF(sin(angle - pi + pi / 3) * size, cos(angle - pi + pi / 3) * size)

            self.arrow_head.clear()
            self.arrow_head.append(self.line().p2())
            self.arrow_head.append(arrow_p1)
            self.arrow_head.append(arrow_p2)
            painter.drawPolygon(self.arrow_head)

            self.parent.diagramScene.update()

