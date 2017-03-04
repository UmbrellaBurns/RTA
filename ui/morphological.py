from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MorphologicalAnalysisWidget(QWidget):
    def __init__(self, content=None, parent=None):
        super(MorphologicalAnalysisWidget, self).__init__(parent)

        self.__markup_view = QWebEngineView(self)
        self.__legend = None

        self.__content = content

        if content is not None:
            self.__markup_view.setHtml(self.__content)

        self.setup_ui()

    def setup_ui(self):

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.__markup_view)

        self.setLayout(hbox_layout)

    def load_from_markup_doc(self, source_text):
        self.__markup_view.setHtml(source_text)

