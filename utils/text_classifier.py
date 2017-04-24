from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QLabel, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtWidgets import QSizePolicy
import PyQt5.QtGui as QtGui
from statistical_analysis.statistical import StatisticalAnalysis
from utils.category_dialog import CategoryDialog


class TextClassificationWidget(QWidget):
    def __init__(self, content=None, classifier=None, parent=None):
        super(TextClassificationWidget, self).__init__(parent)

        self.setWindowTitle("Классификатор текста")

        if classifier is None:
            self.__classifier = StatisticalAnalysis()
            self.__classifier.train_classifier()
        else:
            self.__classifier = classifier

        self.__text_edit = QTextEdit()
        self.__classify = QPushButton("Анализ")
        self.__correction = QPushButton("Правка")

        self.__text_category = QLabel()

        self.setup_ui()

    def setup_ui(self):

        self.__classify.clicked.connect(self.__processing)
        self.__correction.clicked.connect(self.__update_classifier)

        label_style = """
                            background-color: rgb(150, 210, 57);
                            border-radius: 5px;
                            padding: 5px;
                            color: white;
                            border: 2px solid rgb(150, 210, 57);
                        """

        self.__text_category.setStyleSheet(label_style)
        category = "<h2>Категория текста:</h2>"
        self.__text_category.setText(category)

        self.__correction.setEnabled(False)

        # setup layout

        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        vbox = QVBoxLayout()
        vbox.addWidget(self.__classify)
        vbox.addWidget(self.__correction)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.__text_category)
        hbox_layout.addItem(spacer)
        hbox_layout.addLayout(vbox)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.__text_edit)
        vbox_layout.addItem(hbox_layout)

        self.setLayout(vbox_layout)

    def __processing(self):
        """
        Processing text classification
        """

        if len(self.__text_edit.toPlainText()) > 0:

            self.__classifier.set_text(self.__text_edit.toPlainText())

            # Processing statistical analysis
            self.__classifier.analysis()

            category = "<h2>Категория текста: {0}</h2>".format(self.__classifier.get_text_category())
            self.__text_category.setText(category)

            self.__correction.setEnabled(True)

    def __update_classifier(self):
        """
        Change category manually & update classifier
        """

        msg = QMessageBox()

        msg.setIcon(QMessageBox.Question)
        msg.setText("Переобучить классификатор?")
        msg.setInformativeText("Это действие нельзя отменить")
        msg.setWindowTitle("Смена категории")
        msg.setDetailedText("Обновление классификатора может занять несколько секунд." +
                            "Для приведения классификатора в исходное состояние необходимо заменить в папке " +
                            "'rta/common' файл 'rss-all.sqlite' на файл 'backup_rss-all.sqlite' и изменить имя файла " +
                            "обратно на 'rss-all.sqlite'")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        confirm = msg.exec_()

        if confirm == QMessageBox.Ok:
            cd = CategoryDialog()
            cd.setWindowTitle("Выберите категорию")

            cd.exec_()

            category = self.__classifier.get_category_by_cyr_repr(cd.value())
            cat = cd.value()
            if category is not None:
                self.__classifier.update_classifier_data(self.__text_edit.toPlainText(), category)
