from syntax_analysis.xml_to_tree import XmlToTree
from syntax_analysis.tree_to_graphviz import TreeToGraphviz
from PyQt5 import QtWidgets, QtSvg
from PyQt5.Qt import QByteArray
import sys
import os
import subprocess


class SyntaxAnalysis:
    """
    Syntax analysis module:
    """
    def __init__(self, text=None):
        self.__text = text

        self.__parser = None

        self.__tree_to_graphviz = None

        self.__sentences = None

    def set_text(self, text):
        self.__text = text

    def __pre_processing(self):
        """
        Create text file and parse it with solarix parser.
        Next - parse xml tree and visualize it with graphviz.
        :return xml syntax tree
        """

        output = os.getcwd() + '/parsing-tree.xml'
        parser_dir = os.getcwd() + '/solarix_parser/'

        input_file = parser_dir + 'input.txt'

        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(self.__text)

        cmd = parser_dir + 'Parser.exe -parser 0 -emit_morph 0 -eol -d ' \
              + parser_dir + 'dictionary.xml ' + input_file + ' -o ' \
              + output

        PIPE = subprocess.PIPE
        p = subprocess.Popen(cmd, shell=False)
        p.wait()

        return output

    def get_triples(self):
        """
        :return: List of triples -> [Node, Relation, Node]
        """

        triples = []

        if self.__sentences is not None:
            for sentence in self.__sentences:

                # Get syntax tree of each sentence
                tree = sentence.get_syntax_tree()

                for node in tree.get_nodes():
                    if node.get_parent() is not None:
                        triples.append([node.get_parent().get_word(), node.get_link_type(), node.get_word()])

        return triples

    def analysis(self):
        """
        Syntax analysis
        :return dict {sentences[] : svg_trees[]}
        """

        xml = self.__pre_processing()

        self.__parser = XmlToTree(xml)

        self.__sentences = self.__parser.parse()

        self.__tree_to_graphviz = TreeToGraphviz()

        # Sentence => SVG-tree
        data = {}

        for sentence in self.__sentences:
            svg = self.__tree_to_graphviz.get_svg_tree(sentence)
            data[sentence.get_text()] = svg

        return data


