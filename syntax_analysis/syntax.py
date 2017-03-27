from syntax_analysis.xml_to_tree import XmlToTree
from syntax_analysis.tree_to_graphviz import TreeToGraphviz
from PyQt5 import QtWidgets, QtSvg
from PyQt5.Qt import QByteArray
import sys


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    file = 'parsing-tree.xml'

    parser = XmlToTree(file)

    sentences = parser.parse()

    tree_to_graphviz = TreeToGraphviz()

    svg = tree_to_graphviz.get_svg_tree(sentences[0])

    byte_array = QByteArray()
    byte_array.append(svg)

    svg_view = QtSvg.QSvgWidget()

    svg_view.load(byte_array)

    svg_view.show()

    sys.exit(app.exec_())

