from textblob import TextBlob
from morphological_analysis.pymorphy_wrap import MorphAnalyzer
import re
import os
from collections import OrderedDict
import numpy as np
from common.e_text_category import TextCategory
import sqlite3

from Stemmer import Stemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


class StatisticalAnalysis:
    """
    Statistical analysis module, which includes:
    - Text classification
    - Creation of semantic core
    - Statistical information about the text
    """
    def __init__(self, text):
        self.__text = text

        self.__tokens = None

        self.__morph_analyzer = MorphAnalyzer()

        self.__frequency = None

        self.__category = None

        self.__text_classifier = None

        self.__common_dir = os.getcwd() + '/common/'

        self.__pre_processing()

    def analysis(self):
        """
        Complex statistical analysis
        """

        unsorted_frequency = {}

        stop_words = []

        with open(self.__common_dir + 'stop-words.txt', 'r', encoding='utf-8') as f:
            stop_words = f.read().split('\n')

        for token in self.__tokens:
            if token not in stop_words:
                unsorted_frequency[token] = self.__word_frequency(token)

        self.__frequency = OrderedDict(sorted(unsorted_frequency.items(), key=lambda x: x[1], reverse=True))

        processed_text = self.__text_cleaner_with_stemming(self.__text)

        self.__category = self.__predict(text=processed_text)

    def get_words_frequency(self, number=None):
        """
        Returns frequency of all words in the text
        :param number: number of required elements
        :return: dictionary, key - word, value - frequency
        """

        if number is None or number > len(self.__frequency):
            return self.__frequency
        else:
            keys = list(self.__frequency.keys())[:number]
            required = OrderedDict()
            for key in keys:
                required[key] = self.__frequency[key]
            return required

    def get_characters_count(self):
        """
        Returns characters count, including spaces
        """
        return len(self.__text)

    def get_characters_count_without_spaces(self):
        """
        Returns characters count without spaces
        """
        return len(self.__text.replace(" ", ""))

    def get_words_count(self):
        return len(self.__tokens)

    def get_text_category(self):
        """
        Returns the text category obtained using TF-IDF
        """
        return self.__get_cyr_category_repr(self.__category)

    def __pre_processing(self):
        """
        Text tokenization. Text classifier initialization
        """

        blob = TextBlob(self.__text_cleaner(self.__text))
        self.__tokens = list(blob.tokens)

        self.__normalize_tokens()

        data = self.__load_classifier_data()

        # Cleaning the training data
        data['text'] = [self.__text_cleaner_with_stemming(t) for t in data['text']]

        # Split the training data
        d = self.__split_training_data(data)

        # Training the classifier
        self.__text_classifier = Pipeline([
            ('hashvect', HashingVectorizer()),
            ('tfidf', TfidfTransformer(use_idf=False)),
            ('clf', SGDClassifier(loss='hinge')),
        ])

        self.__text_classifier.fit(d['train']['x'], d['train']['y'])

    def __predict(self, text):
        """
        Predicting of the category of the text
        :param text: source raw text
        :return: one of 13 categories
        """

        source_text = [self.__text_cleaner_with_stemming(text)]
        predicted = self.__text_classifier.predict(source_text)

        str_category = predicted[0]

        text_category = None

        if str_category == 'politics':
            text_category = TextCategory.POLITICS
        elif str_category == 'culture':
            text_category = TextCategory.CULTURE
        elif str_category == 'sport':
            text_category = TextCategory.SPORT
        elif str_category == 'health':
            text_category = TextCategory.HEALTH
        elif str_category == 'tech':
            text_category = TextCategory.TECH
        elif str_category == 'economics':
            text_category = TextCategory.ECONOMICS
        elif str_category == 'incident':
            text_category = TextCategory.INCIDENT
        elif str_category == 'auto':
            text_category = TextCategory.AUTO
        elif str_category == 'woman':
            text_category = TextCategory.WOMAN
        elif str_category == 'advertising':
            text_category = TextCategory.ADVERTISING
        elif str_category == 'social':
            text_category = TextCategory.SOCIAL
        elif str_category == 'realty':
            text_category = TextCategory.REALTY
        elif str_category == 'science':
            text_category = TextCategory.SCIENCE
            
        return text_category

    @staticmethod
    def __get_cyr_category_repr(category):
        """
        Returns cyrillic string representation of text category
        :param category: one of TextCategory enumeration
        :return: category string
        """

        if category == TextCategory.POLITICS:
            return "ПОЛИТИКА"
        elif category == TextCategory.CULTURE:
            return "КУЛЬТУРА"
        elif category == TextCategory.SPORT:
            return "СПОРТ"
        elif category == TextCategory.HEALTH:
            return "ЗДОРОВЬЕ"
        elif category == TextCategory.TECH:
            return "ТЕХНОЛОГИИ"
        elif category == TextCategory.ECONOMICS:
            return "ЭКОНОМИКА"
        elif category == TextCategory.INCIDENT:
            return "ИНЦИДЕНТ"
        elif category == TextCategory.AUTO:
            return "ТРАНСПОРТ"
        elif category == TextCategory.WOMAN:
            return "ЖЕНЩИНЫ"
        elif category == TextCategory.ADVERTISING:
            return "РЕКЛАМА"
        elif category == TextCategory.SOCIAL:
            return "СОЦИАЛЬНАЯ СФЕРА"
        elif category == TextCategory.REALTY:
            return "НЕДВИЖИМОСТЬ"
        elif category == TextCategory.SCIENCE:
            return "НАУКА"

    def __load_classifier_data(self):
        """
        Loading rss-feed from sqlite database

        :return: dictionary, which contains list of texts and list of their categories
        """

        db_name = self.__common_dir + 'rss-all.sqlite'

        data = {'text': [], 'tag': []}

        conn = sqlite3.connect(db_name)
        try:
            c = conn.cursor()
            for row in c.execute('SELECT * FROM data'):
                data['text'] += [row[1]]
                data['tag'] += [row[2]]
        finally:
            conn.close()

        return data

    @staticmethod
    def __split_training_data(data, validation_split=0.0):
        """
        Split source texts into two parts: training and testing
        :param data: source texts
        :param validation_split: proportions
        :return: dict, which contains training and testing data
        """

        sz = len(data['text'])
        indices = np.arange(sz)
        np.random.shuffle(indices)

        X = [data['text'][i] for i in indices]
        Y = [data['tag'][i] for i in indices]
        nb_validation_samples = int(validation_split * sz)

        return {
            'train': {'x': X[-nb_validation_samples:], 'y': Y[-nb_validation_samples:]},
            'test': {'x': X[:-nb_validation_samples], 'y': Y[:-nb_validation_samples]}
        }

    def __normalize_tokens(self):
        """
        Replace tokens with their normal form
        """
        normalized = []

        for token in self.__tokens:
            target = self.__morph_analyzer.get_best_parse_result(token)
            normalized.append(target.normal_form)

        self.__tokens = normalized

    def __entry_count(self, word):
        """
        Find the number of occurrences of word in the text
        :param word: Target word
        :return: number of occurrences
        """
        count = 0
        for token in self.__tokens:
            if token == word:
                count += 1

        return count

    def __word_frequency(self, word, entry_count=None):
        """
        Find the frequency of source word in the text
        :param word: source word
        :param entry_count: the number of occurrences of word in the text
        :return: frequency (in persents)
        """
        if entry_count is not None:
            return round(100 * entry_count / len(self.__tokens), 2)
        else:
            return round(100 * self.__entry_count(word) / len(self.__tokens), 2)

    @staticmethod
    def __text_cleaner(raw_text):
        """
        Using regexp to clean up the text

        :param raw_text: source text
        :return: clean text
        """

        raw_text = raw_text.lower()  # приведение в lowercase,

        raw_text = re.sub(r'https?://[\S]+', ' url ', raw_text)  # замена интернет ссылок
        raw_text = re.sub(r'[\w\./]+\.[a-z]+', ' url ', raw_text)

        raw_text = re.sub(r'\d+[-/\.]\d+[-/\.]\d+', ' date ', raw_text)  # замена даты и времени
        raw_text = re.sub(r'\d+ ?гг?', ' date ', raw_text)
        raw_text = re.sub(r'\d+:\d+(:\d+)?', ' time ', raw_text)
        raw_text = re.sub(r'@\w+', ' tname ', raw_text)  # замена имён twiter
        raw_text = re.sub(r'#\w+', ' htag ', raw_text)  # замена хештегов

        raw_text = re.sub(r'<[^>]*>', ' ', raw_text)  # удаление html тагов
        raw_text = re.sub(r'[\W]+', ' ', raw_text)  # удаление лишних символов

        stw = ['в', 'по', 'на', 'из', 'и', 'или', 'не', 'но', 'за', 'над', 'под', 'то',
               'a', 'at', 'on', 'of', 'and', 'or', 'in', 'for', 'at']
        remove = r'\b(' + '|'.join(stw) + ')\b'
        raw_text = re.sub(remove, ' ', raw_text)

        raw_text = re.sub(r'\b\w\b', ' ', raw_text)  # удаление отдельно стоящих букв

        raw_text = re.sub(r'\b\d+\b', ' digit ', raw_text)  # замена цифр

        return raw_text

    @staticmethod
    def __text_cleaner_with_stemming(raw_text):
        """
        Using regexp to clean up the text
        Stemming the text

        :param raw_text: source text
        :return: clean text
        """

        raw_text = raw_text.lower()  # приведение в lowercase,

        raw_text = re.sub(r'https?://[\S]+', ' url ', raw_text)  # замена интернет ссылок
        raw_text = re.sub(r'[\w\./]+\.[a-z]+', ' url ', raw_text)

        raw_text = re.sub(r'\d+[-/\.]\d+[-/\.]\d+', ' date ', raw_text)  # замена даты и времени
        raw_text = re.sub(r'\d+ ?гг?', ' date ', raw_text)
        raw_text = re.sub(r'\d+:\d+(:\d+)?', ' time ', raw_text)
        raw_text = re.sub(r'@\w+', ' tname ', raw_text)  # замена имён twiter
        raw_text = re.sub(r'#\w+', ' htag ', raw_text)  # замена хештегов

        raw_text = re.sub(r'<[^>]*>', ' ', raw_text)  # удаление html тагов
        raw_text = re.sub(r'[\W]+', ' ', raw_text)  # удаление лишних символов

        stemmer = Stemmer('russian')

        raw_text = ' '.join(stemmer.stemWords(raw_text.split()))

        stw = ['в', 'по', 'на', 'из', 'и', 'или', 'не', 'но', 'за', 'над', 'под', 'то',
               'a', 'at', 'on', 'of', 'and', 'or', 'in', 'for', 'at']
        remove = r'\b(' + '|'.join(stw) + ')\b'
        raw_text = re.sub(remove, ' ', raw_text)

        raw_text = re.sub(r'\b\w\b', ' ', raw_text)  # удаление отдельно стоящих букв

        raw_text = re.sub(r'\b\d+\b', ' digit ', raw_text)  # замена цифр

        return raw_text
