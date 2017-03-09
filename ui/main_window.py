from PyQt5.QtWidgets import QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QTextEdit, \
    QMenu, QAction, QStyle, qApp, QListWidget, QStackedWidget, QFormLayout, QSplitter, QFileDialog
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from solarix_parser.syntax import SyntaxAnalyzer
from graphematical_analysis.graphematical import GraphematicalAnalyser
from graphematical_analysis.graphematical_markup import GraphematicalMarkup
from ui.graphematical import GraphematicalAnalysisWidget
from morphological_analysis.morphological import MorphologicalAnalysis
from morphological_analysis.morphological_markup import MorphologicalMarkup
from ui.morphological import MorphologicalAnalysisWidget
from statistical_analysis.statistical import StatisticalAnalysis
from ui.statistical import StatisticalAnalysisWidget


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.__text = None  # source text

        self.__doc = None

        self.__left_bar = None  # list widget, which can change widgets on a __stacked_widget
        self.__stacked_widget = None  # stacked widget, which contains results of analysis

        # __stacked_widget items
        self.__text_edit = None  # source text editor
        self.__graphematical = None  # graphematical analyser
        self.__morphological = None  # morphological analyser
        self.__statistical = None  # statistical analyser
        self.__syntactical = None  # syntactical analyser
        self.__semantic = None  # semantic analyser
        self.__complex = None  # complex analyser, which includes all of previous

        self.__tasks_queue = None

        # Setup Ui
        self.__setup_ui()

    def __setup_ui(self):
        # main window settings
        self.setMinimumSize(QSize(480, 80))
        self.setWindowTitle("RTA - Russian Text Analyzer")

        # central widget setup
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # left bar & stacked widget setup
        self.__left_bar = QListWidget(central_widget)
        self.__stacked_widget = QStackedWidget(central_widget)
        self.__left_bar.setMaximumWidth(150)

        self.__left_bar.currentRowChanged.connect(self.__display)  # change widget on a __stacked_widget

        # creating menu
        # Setup Menu
        bar = self.menuBar()

        file = bar.addMenu("Файл")
        file.addAction("Открыть")
        file.triggered[QAction].connect(self.__open_file)

        analysis = bar.addMenu("Анализ")
        self.__action_start = analysis.addAction("Начать анализ")
        analysis.addSeparator()
        self.__action_graphematical = analysis.addAction("Графематический анализ")
        self.__action_morphological = analysis.addAction("Морфологический анализ")
        self.__action_statistical = analysis.addAction("Статистический анализ")
        self.__action_syntactical = analysis.addAction("Синтаксический анализ")
        self.__action_semantic = analysis.addAction("Семантический анализ")
        self.__action_complex = analysis.addAction("Комплексный анализ")

        analysis.triggered[QAction].connect(self.__process_analysis_menu)

        self.__action_graphematical.setCheckable(True)
        self.__action_morphological.setCheckable(True)
        self.__action_statistical.setCheckable(True)
        self.__action_syntactical.setCheckable(True)
        self.__action_semantic.setCheckable(True)
        self.__action_complex.setCheckable(True)

        help = bar.addMenu("Помощь")

        # analysers creating & setup
        self.__text_edit = QTextEdit()
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

            i = self.__stacked_widget.count()

            for i in range(self.__stacked_widget.count() - 1, 0, -1):
                widget = self.__stacked_widget.widget(i)
                self.__stacked_widget.removeWidget(widget)
                widget.deleteLater()

            i = self.__stacked_widget.count()
            # Start analysis
            self.__start_analysis()

    def __start_analysis(self):

        # Reset all
        self.__graphematical = None  # graphematical analyser
        self.__morphological = None  # morphological analyser
        self.__statistical = None  # statistical analyser
        self.__syntactical = None  # syntactical analyser
        self.__semantic = None  # semantic analyser
        self.__complex = None  # complex analyser, which includes all of previous

        if self.__action_complex.isChecked():
            # Processing all of analysis
            pass
        else:
            if self.__action_graphematical.isChecked():
                # Processing graphematical analysis
                self.__graphematical = GraphematicalAnalyser(text=self.__text_edit.toPlainText())
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

            if self.__action_morphological.isChecked():

                if self.__graphematical is not None:
                    self.__morphological = MorphologicalAnalysis(text=self.__text_edit.toPlainText(),
                                                                 tokens=self.__graphematical.get_tokens())

                else:
                    self.__morphological = MorphologicalAnalysis(text=self.__text_edit.toPlainText())

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

            if self.__action_statistical.isChecked():
                self.__statistical = StatisticalAnalysis(text=self.__text_edit.toPlainText())

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

    def __text_processing(self):

        text = self.text_edit.toPlainText()

        with open('input.txt', 'w', encoding='utf-8') as f:
            f.write(text)

        syntax_analyzer = SyntaxAnalyzer('input.txt')
        syntax_analyzer.analyze()
