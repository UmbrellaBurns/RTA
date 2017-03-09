from PyQt5.QtWidgets import QApplication, QStackedWidget, QLabel, QHBoxLayout, QWidget, QCheckBox, QListWidget, \
    QFormLayout, QLineEdit, QRadioButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtGui, Qt, QtCore


class StatisticalAnalysisWidget(QWidget):
    """
    QWidget, which displays results of statistical analysis
    """

    def __init__(self, parent=None):
        super(StatisticalAnalysisWidget, self).__init__(parent)

        self.__semantic_core_table = QTableWidget(self)
        self.__word_frequency_table = QTableWidget(self)

        self.__statistical_data = QLabel(self)
        self.__label_semantic = QLabel(self)

        self.__label_words = QLabel(self)

        self.__label_semantic.setText("Семантическое ядро")
        self.__label_words.setText("Слова")

        self.__semantic_core_table.setRowCount(0)
        self.__semantic_core_table.setColumnCount(2)
        self.__semantic_core_table.setHorizontalHeaderLabels(["Слово", "Частота"])

        self.__word_frequency_table.setRowCount(0)
        self.__word_frequency_table.setColumnCount(2)
        self.__word_frequency_table.setHorizontalHeaderLabels(["Слово", "Частота"])

        self.__semantic_core_records = 0
        self.__word_frequency_records = 0

        self.__setup_ui()

    def __setup_ui(self):
        """
        Styles & layout setup
        """
        vbox_layout = QVBoxLayout()

        label_style = """
            background-color: rgb(150, 210, 57);
            border-radius: 5px;
            padding: 5px;
            color: white;
            border: 2px solid rgb(150, 210, 57);
        """

        self.__label_semantic.setStyleSheet(label_style)
        self.__label_words.setStyleSheet(label_style)
        self.__statistical_data.setStyleSheet(label_style)

        vbox_layout.addWidget(self.__statistical_data)
        vbox_layout.addWidget(self.__label_semantic)
        vbox_layout.addWidget(self.__semantic_core_table)
        vbox_layout.addWidget(self.__label_words)
        vbox_layout.addWidget(self.__word_frequency_table)

        self.setLayout(vbox_layout)

    def load_from_dict(self, semantic_core, words_frequency):
        """
        Fill tables with values, fetched from dictionary
        :param semantic_core: dictionary, which contains semantic core of the text
        :param words_frequency: dictionary, which contains words and their frequency
        """
        for key in semantic_core:
            new_item = QTableWidgetItem()
            new_item.setText(str(key))
            item_data = QTableWidgetItem()
            item_data.setText(str(semantic_core[key]))
            self.__semantic_core_table.insertRow(self.__semantic_core_records)
            self.__semantic_core_table.setItem(self.__semantic_core_records, 0, new_item)
            self.__semantic_core_table.setItem(self.__semantic_core_records, 1, item_data)
            self.__semantic_core_records += 1

        for key in words_frequency:
            new_item = QTableWidgetItem()
            new_item.setText(str(key))
            item_data = QTableWidgetItem()
            item_data.setText(str(words_frequency[key]))
            self.__word_frequency_table.insertRow(self.__word_frequency_records)
            self.__word_frequency_table.setItem(self.__word_frequency_records, 0, new_item)
            self.__word_frequency_table.setItem(self.__word_frequency_records, 1, item_data)
            self.__word_frequency_records += 1

    def load_statistical_data(self, category, chars_count, chars_count_without_spaces, words_count):
        """
        Fill labels with statistical data
        :param category: the category of the text
        :param chars_count: text length
        :param chars_count_without_spaces: text length without spaces
        :param words_count: number of words in the text
        """

        # statistical_data = """
        # <p>
        # Категория текста:                  {0}</br>
        # Количество символов:               {1}</br>
        # Количество символов без пробелов:  {2}</br>
        # Количество слов:                   {3}</br>
        # </p>
        # """
        statistical_data = """
        <table class="tg">
          <tr>
            <td>Категория текста:</th>
            <td> {0}</th>
          </tr>
          <tr>
            <td>Количество символов:</td>
            <td> {1}</td>
          </tr>
          <tr>
            <td>Количество символов без пробелов:  </td>
            <td> {2}</td>
          </tr>
          <tr>
            <td>Количество слов:</td>
            <td> {3}</td>
          </tr>
        </table>
        """

        statistical_data = statistical_data.format(category, chars_count, chars_count_without_spaces, words_count)

        self.__statistical_data.setText(statistical_data)
