from common.e_label import Grapheme, Label


class Token:
    def __init__(self, text=None, grapheme=None, labels=None, morph=None, morph_cyr=None):
        self.__text = text
        self.__grapheme = grapheme
        self.__labels = labels if labels is not None else []
        self.__morph = morph
        self.__morph_cyr = morph_cyr

    def set_text(self, text):
        self.__text = text

    def set_grapheme(self, grapheme):
        self.__grapheme = grapheme

    def set_labels(self, labels):
        self.__labels = labels

    def set_morph(self, morph):
        self.__morph = morph

    def set_morph_cyr(self, morph_cyr):
        self.__morph_cyr = morph_cyr

    def add_label(self, label):
        self.__labels.append(label)

    def get_text(self):
        return self.__text

    def get_grapheme(self):
        return self.__grapheme

    def get_labels(self):
        return self.__labels

    def get_morph(self):
        return self.__morph

    def get_morph_cyr(self):
        return self.__morph_cyr