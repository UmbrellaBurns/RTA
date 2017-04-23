import sqlite3
from yandex_translate import YandexTranslate, YandexTranslateException


class Translator:
    def __init__(self):

        self.__api_key = 'trnsl.1.1.20170419T213309Z.70ddc54f4fe2d025.fa23b8e218345631f11e83f28520ea417e7e44f9'

        self.__ya_translator = YandexTranslate(self.__api_key)

        self.__con = sqlite3.connect("translator/dictionary.db")

        self.__cur = self.__con.cursor()

    @staticmethod
    def transliterate(word):
        """
        Transliterate russian word to english.
        Ex. Спасибо - Spasibo.
        """

        # Replace spacebars & convert to lower
        word = word.replace(' ', '-').lower()

        transtable = (
            # Большие буквы
            ("Щ", "Sch"),
            ("Щ", "SCH"),
            # two-symbol
            ("Ё", "Yo"),
            ("Ё", "YO"),
            ("Ж", "Zh"),
            ("Ж", "ZH"),
            ("Ц", "Ts"),
            ("Ц", "TS"),
            ("Ч", "Ch"),
            ("Ч", "CH"),
            ("Ш", "Sh"),
            ("Ш", "SH"),
            ("Ы", "Yi"),
            ("Ы", "YI"),
            ("Ю", "Yu"),
            ("Ю", "YU"),
            ("Я", "Ya"),
            ("Я", "YA"),
            # one-symbol
            ("А", "A"),
            ("Б", "B"),
            ("В", "V"),
            ("Г", "G"),
            ("Д", "D"),
            ("Е", "E"),
            ("З", "Z"),
            ("И", "I"),
            ("Й", "J"),
            ("К", "K"),
            ("Л", "L"),
            ("М", "M"),
            ("Н", "N"),
            ("О", "O"),
            ("П", "P"),
            ("Р", "R"),
            ("С", "S"),
            ("Т", "T"),
            ("У", ""),
            ("Ф", "F"),
            ("Х", "H"),
            ("Э", "E"),
            ("Ъ", "`"),
            ("Ь", "'"),
            # Маленькие буквы
            # three-symbols
            ("щ", "sch"),
            # two-symbols
            ("ё", "yo"),
            ("ж", "zh"),
            ("ц", "ts"),
            ("ч", "ch"),
            ("ш", "sh"),
            ("ы", "yi"),
            ("ю", "yu"),
            ("я", "ya"),
            # one-symbol
            ("а", "a"),
            ("б", "b"),
            ("в", "v"),
            ("г", "g"),
            ("д", "d"),
            ("е", "e"),
            ("з", "z"),
            ("и", "i"),
            ("й", "j"),
            ("к", "k"),
            ("л", "l"),
            ("м", "m"),
            ("н", "n"),
            ("о", "o"),
            ("п", "p"),
            ("р", "r"),
            ("с", "s"),
            ("т", "t"),
            ("у", ""),
            ("ф", "f"),
            ("х", "h"),
            ("э", "e"),
        )

        for symbol_in, symbol_out in transtable:
            word = word.replace(symbol_in, symbol_out)

        return word

    def translae(self, word, lang="en"):
        """

        Do translation of input word

        :param word: input word
        :param lang: output lang
        :return: translation result
        """

        if lang == 'en':
            sql_select = """
                            SELECT EN FROM dict WHERE RU = ?
                         """
        else:
            sql_select = """
                            SELECT RU FROM dict WHERE EN = ?
                         """

        # translation = self.__cur.execute(sql_select, word)
        translation = self.__cur.execute(sql_select, [word.lower()]).fetchone()

        if translation is not None:
            return translation[0]
        else:
            try:
                word_forms = self.__ya_translator.translate(word, 'ru-en')['text']
            except YandexTranslateException as e:
                return 'ERR_SERVICE_NOT_AVAILABLE'
            return word_forms[0]

    def add_word(self, ru, en):
        """

        Add new word with translation

        :param ru: russian word
        :param en: english word
        :return: none
        """

        sql_insert = """
        INSERT INTO dict VALUES(?, ?)
        """

        self.__con.execute(sql_insert, (ru, en))

    def __del__(self):

        self.__con.commit()
        self.__con.close()
