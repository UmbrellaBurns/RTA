import graphviz


class TreeToGraphviz:
    def __init__(self):
        self.__node_attrs = {'style': 'filled', 'color': '0.603 0.258 1.000'}
        self.__edge_attrs = {'color': '0.603 0.258 1.000'}

        self.__current_label = 0

        self.__nodes = {}

    def __get_unique_label(self):
        self.__current_label += 1
        return str(self.__current_label)

    def __get_node_by_label(self, label):
        if self.__nodes[label] is not None:
            return self.__nodes[label]
        else:
            return None

    def __get_label_by_node_name(self, name):
        for label in self.__nodes.keys():
            node = self.__nodes[label]
            if name == node[0]:
                return label
        return None

    def get_svg_tree(self, sentence):

        self.__nodes = {}
        self.__current_label = 0

        dot = graphviz.dot.Digraph(comment='parsing-tree', node_attr=self.__node_attrs, edge_attr=self.__edge_attrs)

        nodes = {}

        for node in sentence.get_syntax_tree().get_nodes():

            temp_label = self.__get_unique_label()

            node_parent = node.get_parent()

            if node_parent is None:
                parent_word = None
            else:
                parent_word = node_parent.get_word()

            self.__nodes[temp_label] = [node.get_word(), parent_word, node.get_link_type()]

            dot.node(temp_label, node.get_word())

        for label in self.__nodes.keys():

            node = self.__nodes[label]

            if node[1] is not None:
                parent_label = self.__get_label_by_node_name(node[1])

                dot.edge(parent_label, label, label=node[2])

        dot.format = 'svg'

        return dot.pipe().decode('utf-8')



