from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QSizePolicy
from morphological_analysis.pymorphy_wrap import MorphAnalyzer


class LinguisticAnalysisWidget(QWidget):
    def __init__(self, content=None, parent=None):
        super(LinguisticAnalysisWidget, self).__init__(parent)

        self.setWindowTitle("Лингвистический анализатор")

        self.__morph = MorphAnalyzer()

        self.__line_edit = QLineEdit()
        self.__push_button = QPushButton("Анализ")

        self.__linguistic = QLabel()
        self.__all_results = QLabel()

        self.setup_ui()

    def setup_ui(self):

        regex = QRegExp("[а-я-А-Я]+")

        self.__line_edit.setValidator(QRegExpValidator(regex))

        label_style = """
                    background-color: rgb(150, 210, 57);
                    border-radius: 5px;
                    padding: 5px;
                    color: white;
                    border: 2px solid rgb(150, 210, 57);
                """

        self.__linguistic.setStyleSheet(label_style)
        self.__all_results.setStyleSheet(label_style)

        self.__linguistic.setText('<table class="tg">\n\t<tr>\t\t<th><b>Результаты разбора: </b></th></tr></table>')

        self.__push_button.clicked.connect(self.__processing)

        # setup layout

        hbox_layout = QHBoxLayout()

        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        hbox_layout.addWidget(self.__line_edit)
        hbox_layout.addItem(spacer)
        hbox_layout.addWidget(self.__push_button)

        vbox_layout = QVBoxLayout()

        vbox_layout.addItem(hbox_layout)
        vbox_layout.addWidget(self.__linguistic)
        vbox_layout.addWidget(self.__all_results)
        self.__all_results.hide()

        self.setLayout(vbox_layout)

    def __processing(self):
        """
        Processing linguistic analysis
        """

        self.__all_results.hide()

        target_word = self.__line_edit.text()

        table = '<table class="tg">\n\t<tr>\t\t<th><b>Результаты разбора: </b></th></tr>'
        tr = "\n<tr>\n\t<td>{0}:</td>\n\t<td> {1}</td>\n</tr>"

        parsing_result = self.__morph.parse(target_word)

        analysis_data = {}

        best_result = self.__morph.get_best_parse_result(target_word)

        analysis_data['Часть речи'] = self.__morph.lat2cyr(best_result.tag.POS)

        if best_result.normal_form is not None:
            analysis_data['Нормальная форма'] = best_result.normal_form

        if best_result.tag.animacy is not None:
            analysis_data['Одушевлённость'] = self.__morph.lat2cyr(best_result.tag.animacy)

        if best_result.tag.aspect is not None:
            analysis_data['Вид'] = self.__morph.lat2cyr(best_result.tag.aspect)

        if best_result.tag.case is not None:
            analysis_data['Падеж'] = self.__morph.lat2cyr(best_result.tag.case)

        if best_result.tag.gender is not None:
            analysis_data['Род'] = self.__morph.lat2cyr(best_result.tag.gender)

        if best_result.tag.mood is not None:
            analysis_data['Наклонение'] = self.__morph.lat2cyr(best_result.tag.mood)

        if best_result.tag.number is not None:
            analysis_data['Число'] = self.__morph.lat2cyr(best_result.tag.number)

        if best_result.tag.person is not None:
            analysis_data['Лицо'] = self.__morph.lat2cyr(best_result.tag.person)

        if best_result.tag.tense is not None:
            analysis_data['Время'] = self.__morph.lat2cyr(best_result.tag.tense)

        if best_result.tag.transitivity is not None:
            analysis_data['Переходность'] = self.__morph.lat2cyr(best_result.tag.transitivity)

        if best_result.tag.voice is not None:
            analysis_data['Залог'] = self.__morph.lat2cyr(best_result.tag.voice)

        for category in analysis_data:
            table += tr.format(category, analysis_data[category])

        table += "\n</table>"

        another_results = '<table class="tg">\n\t<tr>\t\t<th><b>Другие результаты: </b></th></tr>'

        for item in parsing_result:
            another_results += "\n<tr>\n\t<td>{0} : </td><td>{1}</td>\n</tr>".format(item.word,
                                                                                     self.__morph.lat2cyr(
                                                                                         item.tag.cyr_repr))

        another_results += "\n</table>"

        if len(parsing_result) > 1:
            self.__all_results.setText(another_results)
            self.__all_results.show()

        self.__linguistic.setText(table)
