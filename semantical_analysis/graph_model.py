class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.observers = []

    def add_node(self, node):
        self.nodes.append(node)
        self.notify_observers()
        # debug
        print('---nodes---')

        for node in self.nodes:
            print(node.text)

        print('---nodes---')

    def remove_node(self, node):
        if node in self.nodes:
            # Удаление всех рёбер, связанных с этим узлом
            self.edges = [edge for edge in self.edges if edge.from_node != node or edge.to_node != node]

            # Удаление самого узла
            self.nodes.remove(node)
            self.notify_observers()

            # debug
            print('---nodes---')

            for node in self.nodes:
                print(node.text)

            print('---nodes---')

    def add_edge(self, from_node, to_node, text):
        if from_node in self.nodes and to_node in self.nodes:
            if from_node != to_node:
                self.edges.append(Edge(from_node, to_node, text))
                self.notify_observers()

                # debug
                print('---all edges---')

                for edge in self.edges:
                    triple = edge.from_node.text + ' ' + edge.text + ' ' + edge.to_node.text
                    print(triple)

                print('---all edges---')

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            self.notify_observers()

            # debug
            print('---all edges---')

            for edge in self.edges:
                triple = edge.from_node.text + ' ' + edge.text + ' ' + edge.to_node.text
                print(triple)

            print('---all edges---')

    def print_edges(self):
        for edge in self.edges:
            triple = edge.from_node.text + ' ' + edge.text + ' ' + edge.to_node.text
            print(triple)

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for item in self.observers:
            item.graph_model_changed()


class Node:
    """
    Class 'Node' it's an implementation of node of graph, which contains some text
    """
    def __init__(self, text):
        self.text = text


class Edge:
    """
        Class 'Edge' it's an implementation of edge of graph, which contains:
        self.from_node - First Node, which leads the edge
        self.to_node - Second Node, which connected with First
        self.text - Type of connection
    """
    def __init__(self, from_node, to_node, text):
        self.from_node = from_node
        self.to_node = to_node
        self.text = text

    def get_first_node(self):
        return self.from_node

    def get_second_node(self):
        return self.to_node

    def get_text(self):
        return self.text
