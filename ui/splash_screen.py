import sys
import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QSplashScreen


class SplashScreen(QSplashScreen):
    """
    Splash screen class that appears during component initialization
    """
    def __init__(self, gif, parent=None):

        self.__movie = QMovie(gif)

        self.__movie.jumpToFrame(0)
        pixmap = QPixmap(self.__movie.frameRect().size())

        QSplashScreen.__init__(self, pixmap)

        self.__movie.frameChanged.connect(self.repaint)

    def processing(self, duration, app):
        """
        Splash screen exec.
        :param duration: duration of splash screen processing
        :param app: application object, required to process events
        """
        start = time.time()

        while self.__movie.state() == QMovie.Running and time.time() < start + duration:
            app.processEvents()

    def showEvent(self, event):
        self.__movie.start()

    def hideEvent(self, event):
        self.__movie.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.__movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.__movie.scaledSize()