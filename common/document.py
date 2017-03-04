from common.e_label import Grapheme, Label


class Document:
    def __init__(self, text=None):

        self.__text = text                  # Plain Text

        self.__sentences = []               # The text, divided into sentences
        self.__tokens = []                  # All of tokens

        # Extracted facts & entities
        self.__links = []
        self.__emails = []
        self.__hash_tags = []
        self.__numbers = []

        self.__text_categories = []         # List of text categorization results

        self.__syntax_tree = None           # XML result of syntactical analysis
        self.__semantic_relations = None    # Graph, result of semantic analysis

    def add_sentence(self, sentence):
        self.__sentences.append(sentence)

    def add_token(self, token):
        self.__tokens.append(token)

    def add_fact(self, token):
        if Label.LINK in token.labels:
            self.__links.append(token)

        if Label.EMAIL in token.labels:
            self.__emails.append(token)

        if Label.HASHTAG in token.labels:
            self.__hashtags.append(token)

        if Label.NUMBER in token.labels:
            self.__numbers.append(token)

    def set_emails(self, emails):
        self.__emails = emails

    def set_links(self, links):
        self.__links = links

    def set_hash_tags(self, hash_tags):
        self.__hash_tags = hash_tags

    def set_tokens(self, tokens):
        self.__tokens = tokens

    def set_sentences(self, sentences):
        self.__sentences = sentences

    def get_tokens(self):
        return self.__tokens

    def get_emails(self):
        return self.__emails

    def get_links(self):
        return self.__links

    def get_hash_tags(self):
        return self.__hash_tags

    def get_sentence(self, i):
        if i in range(0, len(self.__sentences)):
            return self.__sentences[i]
        return None

    def get_token(self, i):
        if i in range(0, len(self.__tokens)):
            return self.__tokens[i]
        return None
