from textblob import TextBlob
from collections import OrderedDict
from common.token import Token
from common.e_label import Grapheme, Label
from common.document import Document
import re
import os


class GraphematicalAnalyser:
    def __init__(self, text):
        self.__text = text

        self.__blob = None

        self.__tokens = []

        self.__DEL = [' ', '  ', '    ', '\t', '\n']
        self.__SIG = ['.', ',', '-', '—', '!', '?', ';', ':', '(', ')', '[', ']', '{', '}']
        self.__SYM = ['«', '»', '\"', '\"', '\"', '``', '\'\'']
        self.__RLE = ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'ф',
                      'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч', 'с',
                      'м', 'и', 'т', 'ь', 'б', 'ю', 'ё',
                      'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ', 'Ф',
                      'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч', 'С',
                      'М', 'И', 'Т', 'Ь', 'Б', 'Ю', 'Ё']

        self.__LLE = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd',
                      'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm',
                      'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D',
                      'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']

        self.__DC = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.__END = ['.', '!', '?']

        self.__emails = []
        self.__hash_tags = []
        self.__links = []

        self.__tokenization_result = []

        self.__doc = None

        self.__regexp_dir = os.getcwd() + '/common/'

        self.__pre_processing()

    def __pre_processing(self):

        # Extract all of emails & replace them with '__EMAIL'
        self.__emails = self.extract_email_addresses(self.__text)
        for email in self.__emails:
            self.__text = self.__text.replace(email, '__EMAIL')

        # Extract all of hashtags & replace them with '__HASHTAG'
        self.__hash_tags = self.extract_hash_tags(self.__text)
        for tag in self.__hash_tags:
            self.__text = self.__text.replace(tag, '__HASHTAG')

        # Extract all of links & replace them with '__LINK'
        self.__links = self.extract_links(self.__text)
        for link in self.__links:
            self.__text = self.__text.replace(link, '__LINK')

        self.__blob = TextBlob(self.__text)

        # Replacing quotes like '``' with "\""
        for token in self.__blob.tokens:
            new_token = str(token)
            if new_token.startswith('``'):
                new_token = "\""
            elif new_token.endswith('\'\''):
                new_token = "\""
            self.__tokenization_result.append(new_token)

        # Removing unicode special character in first token
        self.__tokenization_result[0] = self.__tokenization_result[0][1:]

        quotes = OrderedDict()

        # Searching for quotes, deleting them & remember their positions
        for i in range(0, len(self.__tokenization_result)):
            s = str(self.__tokenization_result[i])
            if self.__tokenization_result[i].startswith("«") or self.__tokenization_result[i].startswith("\""):

                if len(self.__tokenization_result[i]) > 2:
                    # Remember first symbol
                    quotes[i + len(quotes)] = self.__tokenization_result[i][0]

                    # Delete first symbol
                    self.__tokenization_result[i] = self.__tokenization_result[i][1:]

            if self.__tokenization_result[i].endswith("»") or self.__tokenization_result[i].endswith("\""):

                if len(self.__tokenization_result[i]) > 2:
                    # Remember last symbol
                    quotes[i + len(quotes) + 1] = self.__tokenization_result[i][len(self.__tokenization_result[i]) - 1]

                    # Delete last symbol
                    self.__tokenization_result[i] = self.__tokenization_result[i][0:-1]

        # Inserting quotes as individual q
        for key in quotes.keys():
            self.__tokenization_result.insert(key, quotes[key])

    def analysis(self):

        current_email = 0
        current_hash_tag = 0
        current_link = 0

        # Add descriptors & labels for each token in the text
        for raw_token in self.__tokenization_result:

            if raw_token == '__EMAIL':
                raw_token = self.__emails[current_email]
                current_email += 1
            elif raw_token == '__HASHTAG':
                raw_token = self.__hash_tags[current_hash_tag]
                current_hash_tag += 1
            elif raw_token == '__LINK':
                raw_token = self.__links[current_link]
                current_link += 1

            if self.index_of_any(raw_token, self.__DEL):
                # Delimiter
                token = Token(text=raw_token, grapheme=Grapheme.DEL)

                # labels
                token.add_label(Label.SPACE)

                self.__tokens.append(token)

            elif self.index_of_any(raw_token, self.__RLE):
                # Russian lexeme
                token = Token(text=raw_token, grapheme=Grapheme.RLE)

                # labels
                token.add_label(Label.WORD)
                token.add_label(Label.CYRIL)

                self.__tokens.append(token)

            elif self.index_of_any(raw_token, self.__SYM):
                # Symbol
                token = Token(text=raw_token, grapheme=Grapheme.SYM)

                # labels
                token.add_label(Label.QUOTE)
                token.add_label(Label.MARKUP)

                if raw_token == "«" or raw_token == "\"":
                    token.add_label(Label.OPENING)
                elif raw_token == "»" or raw_token == "\"":
                    token.add_label(Label.CLOSING)

                self.__tokens.append(token)

            elif self.index_of_any(raw_token, self.__LLE):
                # Latin lexeme
                token = Token(text=raw_token, grapheme=Grapheme.LLE)

                # labels
                token.add_label(Label.WORD)
                token.add_label(Label.LATIN)

                self.__tokens.append(token)

            elif self.index_of_any(raw_token, self.__DC):
                # Digits complex
                token = Token(text=raw_token, grapheme=Grapheme.DC)

                # labels
                token.add_label(Label.NUMBER)

                self.__tokens.append(token)

            else:
                if self.index_of_any(raw_token, self.__SIG):
                    # Signum
                    token = Token(text=raw_token, grapheme=Grapheme.SIG)

                    # labels
                    token.add_label(Label.PUNCT)

                    if raw_token == "(" or raw_token == "[" or raw_token == '{':
                        token.add_label(Label.OPENING)
                    elif raw_token == ")" or raw_token == "]" or raw_token == '}':
                        token.add_label(Label.CLOSING)

                    self.__tokens.append(token)
                else:
                    # Composite token TODO: add #hashtag, email, phone labels
                    token = Token(text=raw_token, grapheme=Grapheme.COMPOSITE)

                    # labels
                    if raw_token in self.__emails:
                        token.add_label(Label.EMAIL)
                    elif raw_token in self.__hash_tags:
                        token.add_label(Label.HASHTAG)
                    elif raw_token in self.__links:
                        token.add_label(Label.LINK)
                    elif self.is_word_with_a_hyphen(raw_token):
                        token.add_label(Label.WORD)
                        token.add_label(Label.CYRIL)
                    else:
                        token.add_label(Label.OTHER)

                    self.__tokens.append(token)

            space_token = Token(text=" ", grapheme=Grapheme.DEL)
            space_token.add_label(Label.SPACE)

            # self.__tokens.append(space_token)

        return self.__tokens

    @staticmethod
    def index_of_any(source, dictionary):
        for i in range(0, len(source)):
            if source[i] not in dictionary:
                return False
        return True

    @staticmethod
    def intersects(source, dictionary):
        for i in range(0, len(source)):
            if source[i] in dictionary:
                return True
        return False

    @staticmethod
    def extract_email_addresses(string):

        r = re.compile(r'[\w.-]+@[\w.-]+.\w{2,4}')
        return r.findall(string)

    @staticmethod
    def is_word_with_a_hyphen(string):

        r = re.findall(r'[\w-]+[\w-]', string)
        return len(r) > 0

    def extract_links(self, string):

        with open(self.__regexp_dir + 'link_regexp.txt', 'r') as f:
            pattern = f.read()

        r = re.compile(pattern)
        return r.findall(string)

    @staticmethod
    def extract_hash_tags(string):
        r = re.compile(r'#\w*')
        return r.findall(string)

    def get_tokens(self):
        # self.__tokens.pop()
        return self.__tokens

    def get_emails(self):
        return self.__emails

    def get_links(self):
        return self.__links

    def get_hash_tags(self):
        return self.__hash_tags

    def get_document(self):

        self.__doc = Document(text=self.__text)

        self.__doc.set_emails(self.__emails)
        self.__doc.set_links(self.__links)
        self.__doc.set_hash_tags(self.__hash_tags)

        self.__doc.set_tokens(self.__tokens)

        self.__doc.set_sentences(list(self.__blob.sentences))

        return self.__doc
