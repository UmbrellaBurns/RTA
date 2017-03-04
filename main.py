from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

if __name__ == '__main__':
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        w = MainWindow()
        w.resize(700, 500)
        w.show()
        sys.exit(app.exec())

        # TODO: MophologicalAnalysis + pymorphy2 - Singleton, Main Application - Facade.
        # TODO: SyntaxAnalysis: methods - get_syntax_xml_tree, get_raw_xml.
        # TODO: Proposal: make Doc classes - Sentences, Nodes,..
        # TODO: ComplexAnalysis result - xml-doc, which contains document markup, including: text, sentences,
        # TODO: syntax trees with nodes and their relations, semantic graph, text category and more
