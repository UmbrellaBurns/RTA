from xml.dom.minidom import parse
from syntax_analysis.ram import Sentence, SyntaxTree, Node
import os.path


class XmlToTree:
    """
    Convert xml-tree to list of sentences
    """
    def __init__(self, file):

        if os.path.exists(file):
            self.__parser = parse(file)
        else:
            print("'" + file + "' файл не существует.")
            exit(-1)

        self.__parsing_result = []

    def parse(self):
        self.__fetch_data()
        return self.__parsing_result

    def __fetch_data(self):
        """
        Fetch all data from xml-tree
        """

        sentences = self.__parser.getElementsByTagName("sentence")

        if sentences is not None:
            for raw_sentence in sentences:

                sentence = Sentence()

                sentence_text = raw_sentence.getElementsByTagName("text")[0].firstChild.wholeText

                sentence.set_text(sentence_text)

                syntax_tree = SyntaxTree()

                sentence.set_syntax_tree(syntax_tree)

                nodes = raw_sentence.getElementsByTagName("node")

                raw_nodes = []

                for node in nodes:

                    raw_node = {}

                    raw_node['token'] = node.getElementsByTagName("token")[0].firstChild.wholeText
                    raw_node['word'] = node.getElementsByTagName("word")[0].firstChild.wholeText
                    raw_node['parent'] = node.getElementsByTagName("parent")[0].firstChild.wholeText

                    if node.getAttribute('is_root') == 'true':
                        raw_node['link_type'] = ""
                        raw_node['is_root'] = True
                    else:
                        raw_node['link_type'] = node.getElementsByTagName("link_type")[0].firstChild.wholeText
                        raw_node['is_root'] = False

                    raw_nodes.append(raw_node)

                for node in raw_nodes:

                    new_node = Node(node['token'], node['word'])

                    new_node.set_link_type(node['link_type'])

                    syntax_tree.add_node(new_node)

                for i in range(0, len(raw_nodes)):

                    node = syntax_tree.get_node_by_id(raw_nodes[i]['token'])
                    node.set_parent(syntax_tree.get_node_by_id(raw_nodes[i]['parent']))

                    if raw_nodes[i]['is_root']:
                        syntax_tree.set_root(syntax_tree.get_node_by_id(raw_nodes[i]['token']))

                self.__parsing_result.append(sentence)

