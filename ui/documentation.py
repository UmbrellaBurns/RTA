from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os


class DocumentationWidget(QWidget):
    def __init__(self, content=None, parent=None):
        super(DocumentationWidget, self).__init__(parent)

        self.setWindowTitle("Документация")

        self.__docs_view = QWebEngineView(self)

        self.__content = content

        self.__docs_file = os.getcwd() + '/common/docs.html'

        self.load_from_html_doc(self.__docs_file)

        self.setup_ui()

    def setup_ui(self):

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.__docs_view)

        self.setLayout(hbox_layout)

    def load_from_html_doc(self, file_name):

        with open(file_name, 'r', encoding='utf-8') as f:
            self.__content = f.read()

        self.__docs_view.setHtml(self.__content)

