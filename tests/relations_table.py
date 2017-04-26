import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QTableWidget, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QLabel
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QItemDelegate, QTableWidgetItem


class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent):
        super(ComboBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(["None", "CSC", "CI", "CP", "CPVD", "CPVI"])  # Загрузить в список свои данные
        editor.activated.connect(self.emitCommitData)
        return editor

    def setEditorData(self, editor, index):
        pos = 0
        editor.setCurrentIndex(pos)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())

    def emitCommitData(self):
        pass  # сделать то, что требуется, например где-то ещё сохранить


class RelationsToolTip(QWidget):
    def __init__(self, parent=None):
        super(RelationsToolTip, self).__init__(parent)

        self.setWindowTitle("Типы отношений")

        self.__label = QLabel()

        label_style = """
                    background-color: rgb(150, 210, 57);
                    border-radius: 5px;
                    padding: 5px;
                    color: white;
                    border: 2px solid rgb(150, 210, 57);
                """

        self.__label.setStyleSheet(label_style)

        content = """
            <h1>Типы отношений</h1>

            <h2>CSC - Class-SubClass</h2>
            <h3>Отношение: <i>Класс - Подкласс</i></h3>
            <p>Пример: <i>Гепард - подкласс класса Млекопитающие</i></p>
            <br>

            <h2>CI - Class-Instance</h2>
            <h3>Отношение: <i>Класс - Экземпляр класса</i></h3>
            <p>Пример: <i>Шаблон проектирования - Абстрактная фабрика</i></p>
            <br>

            <h2>CP - Class-Property</h2>
            <h3>Отношение: <i>Класс - Свойство класса</i></h3>
            <p>Пример: <i>Супергерой - Бессмертие</i></p>
            <br>

            <h2>CPVD - Class-Property-Value Direct</h2>
            <h3>Отношение: <i>Класс - прямое свойство класса</i></h3>
            <p>Синтаксис: "класс" - "свойство" - "значение"</p>
            <p>Пример: <i>Фигура - форма - шар</i></p>
            <br>

            <h2>CPVI - Class-Property-Value Indirect</h2>
            <h3>Отношение: <i>Класс - косвенное свойство класса</i></h3>
            <p>Синтаксис: "класс" - "косвенное свойство" - "значение"</p>
            <p>Пример: <i>Автомобиль - содержит - двигатель</i></p>
        """

        self.__label.setText(content)

        # layout setup
        layout = QVBoxLayout()

        layout.addWidget(self.__label)
        self.setLayout(layout)


class RelationsCompletionDialog(QDialog):
    def __init__(self, parent=None, triples=None):
        super(RelationsCompletionDialog, self).__init__(parent)

        self.__relations_table = QTableWidget()

        self.__btn_tool_tip = QPushButton("Подсказка")
        self.__tool_tip = RelationsToolTip()
        self.__btn_accept = QPushButton("Принять")
        self.__btn_skip = QPushButton("Пропустить")

        self.__records = 0

        self.__setup_ui()

        if triples is not None:
            self.load_data(triples)

    def __setup_ui(self):

        self.setWindowModality(1)

        self.__relations_table.setRowCount(0)
        self.__relations_table.setColumnCount(4)
        self.__relations_table.setHorizontalHeaderLabels(["Концепт 1", "Слово-связка", "Концепт 2", "Тип отношения"])

        self.__relations_table.setItemDelegateForColumn(3, ComboBoxDelegate(self))

        self.__btn_accept.clicked.connect(self.__accept)
        self.__btn_skip.clicked.connect(self.__cancel)

        self.__btn_tool_tip.clicked.connect(self.__tool_tip.show)
        self.__btn_tool_tip.setMaximumWidth(100)

        title = """
            <h2>Внимание!<h2>
            <h3>Системе не удалось распознать тип связи для следующих троек. <br>
                Вы можете сделать это вручную или пропустить этот пункт
            </h3>
        """

        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        layout.addWidget(self.__btn_tool_tip)
        layout.addWidget(self.__relations_table)

        hbox_layout = QHBoxLayout()

        hbox_layout.addWidget(self.__btn_accept)
        hbox_layout.addWidget(self.__btn_skip)

        layout.addLayout(hbox_layout)

        self.setLayout(layout)

    def load_data(self, triples):
        """
        Fill the table with triples
        """

        for triple in triples:
            first_concept = QTableWidgetItem(str(triple[0]))
            second_concept = QTableWidgetItem(str(triple[2]))
            link_word = QTableWidgetItem(str(triple[1]))

            self.__relations_table.insertRow(self.__records)
            self.__relations_table.setItem(self.__records, 0, first_concept)
            self.__relations_table.setItem(self.__records, 1, link_word)
            self.__relations_table.setItem(self.__records, 2, second_concept)
            self.__relations_table.setItem(self.__records, 3, QTableWidgetItem('None'))

            self.__records += 1

    def relations(self):

        relations = {
            'None': [],
            'CSC': [],
            'CP': [],
            'CI': [],
            'CPVD': [],
            'CPVI': [],
        }

        for i in range(self.__relations_table.rowCount()):

            first_concept = self.__relations_table.item(i, 0).text()
            link_word = self.__relations_table.item(i, 1).text()
            second_concept = self.__relations_table.item(i, 2).text()
            relation = self.__relations_table.item(i, 3).text()

            relations[relation].append([first_concept, link_word, second_concept])

        return relations

    def __accept(self):
        self.accept()

    def __cancel(self):
        self.close()
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)

    triples = [
        ['Орхидея', 'хз', 'Цветы'],
        ['Gorillaz', 'sub', 'Music Band'],
        ['BMW', 'is an', 'Car'],
        ['Python', 'is an example of', 'Programming Language'],
    ]

    w = RelationsCompletionDialog(triples=triples)
    result = w.exec_()

    if result == 1:
        triples = w.relations()

    sys.exit(app.exec_())
