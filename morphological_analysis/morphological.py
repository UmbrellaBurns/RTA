from morphological_analysis.pymorphy_wrap import MorphAnalyzer
from common.e_label import Grapheme, Label, Morph
from graphematical_analysis.graphematical import GraphematicalAnalyser


class MorphologicalAnalysis:
    def __init__(self, text, tokens=None):
        self.__text = text

        self.__tokens = tokens

        self.__morph_analyzer = MorphAnalyzer()

        self.__pre_processing()

        self.__doc = None

    def __pre_processing(self):

        if self.__tokens is None:
            graphematic_analyzer = GraphematicalAnalyser(text=self.__text)
            graphematic_analyzer.analysis()
            self.__tokens = graphematic_analyzer.get_tokens()
            self.__doc = graphematic_analyzer.get_document()

    def analysis(self):

        # Add morph descriptors for each token in the text
        for token in self.__tokens:

            token_labels = token.get_labels()

            if Label.CYRIL in token_labels:
                result = self.__morph_analyzer.parse(token.get_text())

                # Get result with best score
                result = self.get_parse_by_score(result)

                pos_tag = result.tag.POS

                # Get morph descriptor from tag.POS
                token.set_morph(self.pos_to_morph_label(pos_tag))

                # Get cyril representation of tag
                token.set_morph_cyr(result.tag.cyr_repr)

            else:
                token.set_morph(Morph.OTHER)
                token.set_morph_cyr("Не русская лексема")

        return self.__tokens

    @staticmethod
    def get_parse_by_score(target):
        max_score = target[0].score
        parse_number = 0

        for i in range(1, len(target)):
            if target[i].score > max_score:
                max_score = target[i].score
                parse_number = i

        return target[parse_number]

    @staticmethod
    def pos_to_morph_label(pos):
        if pos == 'NOUN':
            return Morph.NOUN
        elif pos == 'NPRO':
            return Morph.NPRO
        elif pos == 'NUMR':
            return Morph.NUMR
        elif pos == 'ADJF':
            return Morph.ADJF
        elif pos == 'ADJS':
            return Morph.ADJS
        elif pos == 'COMP':
            return Morph.COMP
        elif pos == 'VERB':
            return Morph.VERB
        elif pos == 'INFN':
            return Morph.INFN
        elif pos == 'PRTF':
            return Morph.PRTF
        elif pos == 'PRTS':
            return Morph.PRTS
        elif pos == 'GRND':
            return Morph.GRND
        elif pos == 'ADVB':
            return Morph.ADVB
        elif pos == 'PRED':
            return Morph.PRED
        elif pos == 'PREP':
            return Morph.PREP
        elif pos == 'CONJ':
            return Morph.CONJ
        elif pos == 'PRCL':
            return Morph.PRCL
        elif pos == 'INTJ':
            return Morph.INTJ
        elif pos == 'LATN':
            return Morph.LATN
        else:
            return Morph.OTHER

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
        # Update tokens
        self.__doc.set_tokens(self.__tokens)

        return self.__doc
