import sys
from PyQt5.QtWidgets import QApplication
from tests.graph_editor_test import SemanticAnalysisWidget
from semantical_analysis.graph_model import Graph, Node


if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = Graph()

    triples = [
        ['Млекопитающее', 'есть', 'Животное'],
        ['Млекопитающее', 'имеет', 'Позвоночник'],
        ['Кошка', 'есть', 'Млекопитающее'],
        ['Кошка', 'имеет', 'Шерсть'],
        ['Медведь', 'есть', 'Млекопитающее'],
        ['Медведь', 'имеет', 'Шерсть'],
        ['Кит', 'есть', 'Млекопитающее'],
        ['Кит', 'живёт в', 'Вода'],
        ['Рыба', 'живёт в', 'Вода'],
        ['Рыба', 'есть', 'Животное']
    ]

    for triple in triples:
        c1 = Node(triple[0])
        c2 = Node(triple[2])

        link_type = triple[1]

        model.add_node(c1)
        model.add_node(c2)

        model.add_edge(c1, c2, link_type)

    w = SemanticAnalysisWidget()
    w.load_diagram_from_graph(model)
    w.show()

    sys.exit(app.exec_())
