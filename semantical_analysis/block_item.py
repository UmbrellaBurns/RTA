from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QGraphicsEllipseItem, QMenu, QInputDialog
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QMessageBox
import random


class Block(QGraphicsRectItem):
    """
        Entity-block with text & four connection ports
    """
    def __init__(self, name='Untitled', parent=None):
        super(Block, self).__init__(None)
        self.parent = parent

        w = 60.0
        h = 40.0

        self.__base_color = QColor(158, 94, 155)

        # Properties of the rectangle:
        self.setPen(QtGui.QPen(self.__base_color, 2))
        # self.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
        self.setBrush(QtGui.QBrush(self.__base_color))
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Label:
        self.label = QGraphicsTextItem(name, self)
        self.label.setFont(QFont())
        self.name = name

        # Create corner for resize:
        self.sizer = HandleItem(self)
        self.sizer.setPos(w, h)
        self.sizer.posChangeCallbacks.append(self.changeSize)  # Connect the callback

        self.sizer.setFlag(self.sizer.ItemIsSelectable, True)

        # Inputs and outputs of the block:
        self.ports = []
        self.ports.append(PortItem('a', self))
        self.ports.append(PortItem('b', self))
        self.ports.append(PortItem('c', self))
        self.ports.append(PortItem('d', self))

        # Update size:
        self.changeSize(w, h)

    def get_text(self):
        return self.label.toPlainText()

    def get_random_port(self):
        i = random.randint(0, len(self.ports) - 1)
        if i in range(0, 5):
            return self.ports[i]

    def delete(self):
        msg = QMessageBox()

        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы действительно хотите удалить блок?")
        msg.setInformativeText("Это действие нельзя отменить")
        msg.setWindowTitle("Подтвердите действие")
        msg.setDetailedText("При удалении блока удалятся все его соединения!")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        confirm = msg.exec_()

        if confirm == QMessageBox.Ok:
            self.parent.remove_node(self)

    def edit_parameters(self):
        text, ok = QInputDialog.getText(None, 'Параметры', 'Текст блока:', text=self.label.toPlainText())
        if ok:
            self.label.setPlainText(text)

    def contextMenuEvent(self, event):
        menu = QMenu()
        action_delete = menu.addAction('Удалить')
        action_params = menu.addAction('Параметры')
        action_delete.triggered.connect(self.delete)
        action_params.triggered.connect(self.edit_parameters)
        menu.exec_(event.screenPos())

    def changeSize(self, w, h):
        """ Resize block function """
        # Limit the block size:

        metric = QFontMetrics(self.label.font())
        width = metric.width(self.name)
        height = metric.height()

        if h < height + 5:
            h = height + 5
        if w < width + 5:
            w = width + 5
        self.setRect(0.0, 0.0, w, h)
        # center label:
        rect = self.label.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx = (w - lw) / 2
        ly = (h - lh) / 2
        self.label.setPos(lx, ly)
        # Update port positions:
        self.ports[0].setPos(0, h / 2)
        self.ports[1].setPos(w / 2, 0)
        self.ports[2].setPos(w, h / 2)
        self.ports[3].setPos(w / 2, h)
        return w, h


# Block part:
class PortItem(QGraphicsEllipseItem):
    """ Represents a port to a subsystem """

    def __init__(self, name, parent=None):
        QGraphicsEllipseItem.__init__(self, QRectF(-4, -4, 8.0, 8.0), parent)
        self.parent_block = parent
        self.setCursor(QCursor(QtCore.Qt.CrossCursor))
        # Properties:
        self.setBrush(QBrush(Qt.red))
        # Name:
        self.name = name
        self.posCallbacks = []
        self.setFlag(self.ItemSendsScenePositionChanges, True)

    def itemChange(self, change, value):
        if change == self.ItemScenePositionHasChanged:
            for cb in self.posCallbacks:
                cb(value)
            return value
        return super(PortItem, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.parent_block.parent.start_connection(self)


class HandleItem(QGraphicsEllipseItem):
    """ A handle that can be moved by the mouse """

    def __init__(self, parent=None):
        super(HandleItem, self).__init__(QRectF(-4.0, -4.0, 8.0, 8.0), parent)
        self.posChangeCallbacks = []
        self.setBrush(QtGui.QBrush(Qt.white))
        self.setFlag(self.ItemIsMovable, True)
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setCursor(QtGui.QCursor(Qt.SizeFDiagCursor))

    def itemChange(self, change, value):
        if change == self.ItemPositionChange:
            x, y = value.x(), value.y()
            # TODO: make this a signal?
            # This cannot be a signal because this is not a QObject
            for cb in self.posChangeCallbacks:
                res = cb(x, y)
                if res:
                    x, y = res
                    value = QPointF(x, y)
            return value
        # Call superclass method:
        return super(HandleItem, self).itemChange(change, value)
