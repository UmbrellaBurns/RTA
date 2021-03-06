from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen
from PyQt5.QtGui import QIcon
import sys


def create_window(w):
    w = MainWindow()


if __name__ == '__main__':
    if __name__ == "__main__":
        app = QApplication(sys.argv)

        s = SplashScreen("common/splash.gif")
        s.show()
        s.processing(5, app)

        w = MainWindow()
        w.setWindowIcon(QIcon('ico.png'))
        w.resize(700, 500)

        s.finish(w)

        w.show()
        sys.exit(app.exec())

