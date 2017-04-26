from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QTextEdit, \
    QMenu, QAction, QStyle, qApp, QListWidget, QStackedWidget, QFormLayout, QSplitter, QFileDialog, QProgressBar
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt

# analysis modules
from graphematical_analysis.graphematical import GraphematicalAnalysis
from graphematical_analysis.graphematical_markup import GraphematicalMarkup

from morphological_analysis.morphological import MorphologicalAnalysis
from morphological_analysis.morphological_markup import MorphologicalMarkup

from statistical_analysis.statistical import StatisticalAnalysis
from syntax_analysis.syntax import SyntaxAnalysis
from semantical_analysis.graph_model import Graph, Node

# ui
from ui.graphematical import GraphematicalAnalysisWidget
from ui.morphological import MorphologicalAnalysisWidget
from ui.statistical import StatisticalAnalysisWidget
from ui.syntax import SyntaxAnalysisWidget
from ui.progress_bar import ProgressBar
from ui.semantical import SemanticAnalysisWidget
from ui.documentation import DocumentationWidget

# utils
from utils.linguistic import LinguisticAnalysisWidget
from utils.text_classifier import TextClassificationWidget


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.__text = None  # source text

        self.__doc = None

        self.__left_bar = None  # list widget, which can change widgets on a __stacked_widget
        self.__stacked_widget = None  # stacked widget, which contains results of analysis

        self.__progress_bar = ProgressBar()
        self.__status_message = QLabel()

        self.__docs_widget = DocumentationWidget()

        # __stacked_widget items
        self.__text_edit = QTextEdit()  # source text editor
        self.__graphematical = GraphematicalAnalysis()  # graphematical analyser
        self.__morphological = MorphologicalAnalysis()  # morphological analyser
        self.__statistical = StatisticalAnalysis()  # statistical analyser
        self.__syntax = SyntaxAnalysis()  # syntax analyser
        self.__semantic = SemanticAnalysisWidget()  # semantic analyser

        # utils items
        self.__utils_semantic = None
        self.__utils_linguistic = None
        self.__utils_text_classification = None

        # Setup Ui
        self.__setup_ui()

    def __setup_ui(self):
        # main window settings
        self.setMinimumSize(QSize(480, 80))
        self.setWindowTitle("RTA - Russian Text Analyzer")

        # central widget setup
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # update status bar
        self.statusBar().show()
        self.statusBar().showMessage("Загрузка компонентов завершена", 4000)

        # left bar & stacked widget setup
        self.__left_bar = QListWidget(central_widget)
        self.__stacked_widget = QStackedWidget(central_widget)
        self.__left_bar.setMaximumWidth(200)

        self.__left_bar.currentRowChanged.connect(self.__display)  # change widget on a __stacked_widget

        # Setup Menu
        bar = self.menuBar()

        file = bar.addMenu("Файл")
        file.addAction("Открыть")
        file.triggered[QAction].connect(self.__open_file)

        analysis_menu = bar.addMenu("Анализ")
        self.__action_start = analysis_menu.addAction("Начать анализ")
        analysis_menu.addSeparator()
        self.__action_graphematical = analysis_menu.addAction("Графематический анализ")
        self.__action_morphological = analysis_menu.addAction("Морфологический анализ")
        self.__action_statistical = analysis_menu.addAction("Статистический анализ")
        self.__action_syntax = analysis_menu.addAction("Синтаксический анализ")
        self.__action_semantic = analysis_menu.addAction("Семантический анализ")
        self.__action_complex = analysis_menu.addAction("Комплексный анализ")

        analysis_menu.triggered[QAction].connect(self.__process_analysis_menu)

        self.__action_graphematical.setCheckable(True)
        self.__action_morphological.setCheckable(True)
        self.__action_statistical.setCheckable(True)
        self.__action_syntax.setCheckable(True)
        self.__action_semantic.setCheckable(True)
        self.__action_complex.setCheckable(True)

        utils_menu = bar.addMenu("Инструменты")
        # self.__action_sentiment = utils_menu.addAction("Сентимент-анализ")
        self.__action_graph_editor = utils_menu.addAction("Редактор графов")
        self.__action_linguistic_analyzer = utils_menu.addAction("Лингвистический анализатор")
        self.__action_text_classifier = utils_menu.addAction("Классификатор текста")

        utils_menu.triggered[QAction].connect(self.__process_utils_menu)

        help_menu = bar.addMenu("Помощь")
        self.__action_docs = help_menu.addAction("Документация")

        help_menu.triggered[QAction].connect(self.__process_help_menu)

        # analysers creating & setup
        self.__left_bar.addItem('Документ')
        self.__stacked_widget.addWidget(self.__text_edit)

        # layout setup
        hbox_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.__left_bar)
        splitter.addWidget(self.__stacked_widget)
        hbox_layout.addWidget(splitter)
        central_widget.setLayout(hbox_layout)

    def __display(self, i):
        self.__stacked_widget.setCurrentIndex(i)

    def __show_on_status_bar(self, message):
        self.__status_message.setText(message)

    def __open_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Открыть файл', '')[0]

        if len(file_name) > 0:
            with open(file_name, 'r', encoding='utf-8') as f:
                self.__text_edit.setText(f.read())

            self.__text = self.__text_edit.toPlainText()

    def __process_analysis_menu(self, menu_item):
        if menu_item.text() == "Начать анализ":

            self.__left_bar.clear()
            self.__left_bar.addItem('Документ')

            for i in range(self.__stacked_widget.count() - 1, 0, -1):
                widget = self.__stacked_widget.widget(i)
                self.__stacked_widget.removeWidget(widget)
                widget.deleteLater()

            # Start analysis
            self.__start_analysis()

    def __process_utils_menu(self, menu_item):
        if menu_item.text() == "Анализ Тональности":
            pass
        elif menu_item.text() == "Редактор графов":
            # open an semantic analysis widget
            self.__utils_semantic = SemanticAnalysisWidget()
            self.__utils_semantic.setWindowTitle("Редактор графов")
            self.__utils_semantic.show()

        elif menu_item.text() == "Лингвистический анализатор":
            # open an linguistic analysis widget
            self.__utils_linguistic = LinguisticAnalysisWidget()
            self.__utils_linguistic.show()

        elif menu_item.text() == "Классификатор текста":
            # open an text classifier widget
            self.__utils_text_classification = TextClassificationWidget(classifier=self.__statistical)
            self.__utils_text_classification.show()

    def __process_help_menu(self, menu_item):
        if menu_item.text() == "Документация":
            self.__docs_widget.show()

    def __graphematical_analysis(self):
        """
        This method performs graphematical analysis and display results
        """

        # update status bar
        self.__show_on_status_bar("Графематический анализ..")

        # Processing graphematical analysis
        self.__graphematical.set_text(text=self.__text_edit.toPlainText())
        self.__graphematical.analysis()

        # Building markup
        graphematical_markup = GraphematicalMarkup()
        graphematical_markup.generate_from_tokens(self.__graphematical.get_tokens())

        # Setup View
        graphematical_widget = GraphematicalAnalysisWidget(content=graphematical_markup.get_document())
        self.__left_bar.addItem('Графематический анализ')
        self.__stacked_widget.addWidget(graphematical_widget)
        graphematical_widget.show()

        # Get document from graphematical analyser
        self.__doc = self.__graphematical.get_document()

    def __morphological_analysis(self):
        """
        This method performs morphological analysis and display results
        """

        # update status bar
        self.__show_on_status_bar("Морфологический анализ..")

        if self.__action_graphematical.isChecked():
            self.__morphological.set_tokens(self.__graphematical.get_tokens())
        else:
            self.__morphological.set_text(self.__text_edit.toPlainText())

        # Processing morphological analysis
        self.__morphological.analysis()

        # Building markup
        morphological_markup = MorphologicalMarkup()
        morphological_markup.generate_from_tokens(self.__morphological.get_tokens())

        # Setup View
        morphological_widget = MorphologicalAnalysisWidget(content=morphological_markup.get_document())
        self.__left_bar.addItem('Морфологический анализ')
        self.__stacked_widget.addWidget(morphological_widget)
        morphological_widget.show()

    def __statistical_analysis(self):
        """
        This method performs statistical analysis and display results
        """

        # update status bar
        self.__show_on_status_bar("Статистический анализ..")

        self.__statistical.set_text(self.__text_edit.toPlainText())

        # Processing statistical analysis
        self.__statistical.analysis()

        # Setup View
        statistical_widget = StatisticalAnalysisWidget()

        semantic_core = self.__statistical.get_words_frequency(10)
        words_frequency = self.__statistical.get_words_frequency()

        category = self.__statistical.get_text_category()
        chars_count = self.__statistical.get_characters_count()
        chars_count_without_spaces = self.__statistical.get_characters_count_without_spaces()
        words_count = self.__statistical.get_words_count()

        statistical_widget.load_from_dict(semantic_core, words_frequency)
        statistical_widget.load_statistical_data(category, chars_count, chars_count_without_spaces, words_count)

        self.__left_bar.addItem('Статистический анализ')
        self.__stacked_widget.addWidget(statistical_widget)
        statistical_widget.show()

    def __syntactical_analysis(self):
        """
        This method performs syntactical analysis and display results
        """

        # update status bar
        self.__show_on_status_bar("Синтаксический анализ..")

        self.__syntax.set_text(self.__text_edit.toPlainText())

        # Processing statistical analysis
        data = self.__syntax.analysis()

        # Setup View
        syntax_widget = SyntaxAnalysisWidget()

        syntax_widget.load_data(data)

        self.__left_bar.addItem('Синтаксический анализ')
        self.__stacked_widget.addWidget(syntax_widget)
        syntax_widget.show()

    def __semantic_analysis(self):
        """
        This method performs semantic analysis and display results
        """

        self.__show_on_status_bar("Семантический анализ..")

        if not self.__action_syntax.isChecked():
            self.__syntax.set_text(self.__text_edit.toPlainText())

            # Processing statistical analysis
            self.__syntax.analysis()

            raw_triples = self.__syntax.get_triples()

        else:
            raw_triples = self.__syntax.get_triples()

        triples = []

        for triple in raw_triples:
            if triple[1] in ['SUBJECT', 'OBJECT', 'ATTRIBUTE', 'RIGHT_GENITIVE_OBJECT', 'RHEMA']:
                triples.append([triple[0], triple[1], triple[2]])

        model = Graph()

        for triple in triples:
            c1 = Node(triple[0])
            c2 = Node(triple[2])

            link_type = triple[1]

            model.add_node(c1)
            model.add_node(c2)

            model.add_edge(c1, c2, link_type)

        # TODO: Randomize nodes position

        self.__semantic = SemanticAnalysisWidget()
        self.__semantic.load_diagram_from_graph(model)
        self.__left_bar.addItem('Семантический анализ')
        self.__stacked_widget.addWidget(self.__semantic)
        self.__semantic.show()

    def __start_analysis(self):

        self.__show_on_status_bar("Анализ..")
        self.statusBar().addWidget(self.__status_message, 2)
        self.statusBar().addWidget(self.__progress_bar, 1)

        self.__progress_bar.set_value(0)

        # Reset all
        # self.__graphematical = None  # graphematical analyser
        # self.__morphological = None  # morphological analyser
        # self.__statistical = None  # statistical analyser
        # self.__syntactical = None  # syntactical analyser
        # self.__semantic = None  # semantic analyser
        # self.__complex = None  # complex analyser, which includes all of previous

        if self.__action_complex.isChecked():
            # Processing all of analysis

            self.__graphematical_analysis()
            self.__progress_bar.set_value(20)

            self.__morphological_analysis()
            self.__progress_bar.set_value(45)

            self.__statistical_analysis()
            self.__progress_bar.set_value(63)

            self.__syntactical_analysis()
            self.__progress_bar.set_value(79)

            self.__semantic_analysis()
            self.__show_on_status_bar("Готово")
            self.__progress_bar.set_value(100)

        else:
            # Processing selected types of analysis

            if self.__action_graphematical.isChecked():

                self.__graphematical_analysis()

            self.__progress_bar.set_value(20)

            if self.__action_morphological.isChecked():

                self.__morphological_analysis()

            self.__progress_bar.set_value(45)

            if self.__action_statistical.isChecked():

                self.__statistical_analysis()

            self.__progress_bar.set_value(63)
                
            if self.__action_syntax.isChecked():

                self.__syntactical_analysis()

            self.__progress_bar.set_value(79)

            if self.__action_semantic.isChecked():

                self.__semantic_analysis()

            self.__show_on_status_bar("Готово")
            self.__progress_bar.set_value(100)

