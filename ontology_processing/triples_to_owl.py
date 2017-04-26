from ontology_processing.owl_encoder import OWLEncoder
from ontology_processing.utils import RelationsCompletionDialog
from translator.translate import Translator
from nltk.corpus import wordnet
import pymorphy2


class TriplesToOWL:
    """
    Class, which provides triples translation to owl-entities
    """

    def __init__(self, triples):

        self.__triples = triples

        self.__concepts_set = set()
        self.__link_words_set = set()
        self.__unions_dict = dict()
        self.__restrictions_dict = dict()
        self.__translator = Translator()
        self.__morph = pymorphy2.MorphAnalyzer()

        # Lists of link-words, that belongs to each category
        self.__csc = []
        self.__cp = []
        self.__ci = []
        self.__cpvd = []
        self.__cpvi = []

        self.__owl_encoder = OWLEncoder(iri='http://rta.com/ontology.owl')

    def __get_pos_tag(self, word):
        """
        Return part of speech tag of word, using pymorphy2
        """
        return self.__morph.tag(word)[0].POS

    def __init_relation_types_data(self):
        """
        Read link_words from files for each category: CSC, CP, CI, CPVD, CPVI.
        """

        with open("ontology_processing/src/csc.txt", 'r', encoding='utf-8') as f:
            self.__csc = f.read().split('\n')

        self.__csc = [link_word.lower() for link_word in self.__csc]

        with open("ontology_processing/src/ci.txt", 'r', encoding='utf-8') as f:
            self.__ci = f.read().split('\n')

        self.__ci = [link_word.lower() for link_word in self.__ci]

        with open("ontology_processing/src/ci.txt", 'r', encoding='utf-8') as f:
            self.__ci = f.read().split('\n')

        self.__ci = [link_word.lower() for link_word in self.__ci]

        with open("ontology_processing/src/cp.txt", 'r', encoding='utf-8') as f:
            self.__cp = f.read().split('\n')

        self.__cp = [link_word.lower() for link_word in self.__cp]

        with open("ontology_processing/src/cpvd.txt", 'r', encoding='utf-8') as f:
            self.__cpvd = f.read().split('\n')

        self.__cpvd = [link_word.lower() for link_word in self.__cpvd]

        with open("ontology_processing/src/cpvi.txt", 'r', encoding='utf-8') as f:
            self.__cpvi = f.read().split('\n')

        self.__cpvi = [link_word.lower() for link_word in self.__cpvi]

    def __pre_processing(self):
        """
        Extract concepts, unions & restrictions from raw triples
        Triples with single concepts will be removed from the list
        """

        full_triples = []

        for triple in self.__triples:
            if len(triple) == 1:
                self.__concepts_set.add(triple[0])
            else:

                full_triples.append(triple)

                self.__concepts_set.add(triple[0])
                self.__concepts_set.add(triple[2])

                # Add new link word
                self.__link_words_set.add(triple[1])

                # Add new restriction - the case when link-word connect concept c1 to several concepts
                #
                # Key : <Concept 1 Name>_<Link-word>
                # key = '_'.join(triple[:-1])
                #
                # if key in self.__restrictions_dict.keys():
                #     self.__restrictions_dict[key].append(triple[2])
                # else:
                #     self.__restrictions_dict[key] = [triple[2]]

                if triple[1] not in self.__unions_dict.keys():
                    self.__unions_dict[triple[1]] = []

                # Add new union - collect link-words which are common for several triples
                self.__unions_dict[triple[1]].append(triple)

        self.__triples = full_triples

    def __is_csc_relation(self, first_concept, link_word, second_concept):
        """
        Determines whether the triple belongs to CSC-relation
        :return: True or False
        """

        if link_word in self.__csc:
            return True
        else:
            # Translate concepts from 'ru' to 'en' to be able to use nltk.wordnet
            tr_first = self.__translator.translae(first_concept)
            tr_second = self.__translator.translae(second_concept)

            # If YandexTranslate is not available
            if tr_first == 'ERR_SERVICE_NOT_AVAILABLE' or tr_second == 'ERR_SERVICE_NOT_AVAILABLE':
                return False

            tr_first = tr_first.replace(' ', '_')
            tr_second = tr_second.replace(' ', '_')

            s1 = wordnet.synsets(tr_first)
            s2 = wordnet.synsets(tr_second)

            # If synsets were not found
            if len(s1) == 0 or len(s2) == 0:
                return False

            # If both concepts are not Nouns
            if s1[0].pos() != 'n' or s2[0].pos() != 'n':
                return False

            # Use WordNet to extract relation type between two concepts
            # Ex. Cat - Animal => Hyponym - Hyperonym
            c1_hypernyms = []
            c2_hyponyms = []

            for synset in s1:
                if synset.pos() == 'n':
                    c1_hypernyms.append(synset.hypernyms())

            for synset in s2:
                if synset.pos() == 'n':
                    c2_hyponyms.append(synset.hyponyms())

            first_match = False

            for item in c1_hypernyms:
                for hypernym in item:
                    for word_form in hypernym.lemma_names():
                        if word_form.find(tr_second.lower()) > -1 or tr_second.lower().find(word_form) > -1:
                            first_match = True
                            break

            second_match = False

            for item in c2_hyponyms:
                for hyponym in item:
                    for word_form in hyponym.lemma_names():
                        if word_form.find(tr_first.lower()) > -1 or tr_first.lower().find(word_form) > -1:
                            second_match = True
                            break

            return first_match or second_match

    def __is_cpvd_relation(self, first_concept, link_word, second_concept):
        """
        Determines whether the triple belongs to CPVD-relation
        :return: True or False
        """

        if link_word in self.__cpvd:
            return True
        else:
            # if link_word pos tag is NOUN => return True
            for word in wordnet.synsets(link_word):
                if word.pos() == 'n':
                    return True
            return False

    def processing(self):
        """
        Translate triples to owl-entities
        """

        # Extract concepts, unions & restrictions from triples
        self.__pre_processing()

        # Load relation types data
        self.__init_relation_types_data()

        # List of unclassified triples. TODO: categorize manually
        unclassified_triples = []

        # Add all classes to the ontology
        for concept in self.__concepts_set:
            self.__owl_encoder.add_class(concept)

        # Add all unions to the ontology
        for key in self.__unions_dict:
            if len(self.__unions_dict[key]) > 1:
                self.__owl_encoder.add_union(key, self.__unions_dict[key])

        # Add all restrictions to the ontology
        # for key in self.__restrictions_dict:
        #     if len(self.__restrictions_dict[key]) > 1:
        #         self.__owl_encoder.add_restriction(key, self.__restrictions_dict[key])

        # Extract all relations
        for triple in self.__triples:
            first_concept = triple[0]
            link_word = triple[1]
            second_concept = triple[2]

            restriction_key = '_'.join(triple[:-1])

            # # if unions set or restriction set contains current triple - contrinue
            # target_union = self.__owl_encoder.get_union_by_link_word(link_word)
            # # target_restriction = self.__owl_encoder.get_restriction_by_key(restriction_key)
            # if target_union is not None:
            #     if triple in target_union:
            #
            #         if link_word in self.__csc:
            #             pass
            #         elif link_word in self.__ci:
            #             pass
            #         elif link_word in self.__cp:
            #             pass
            #         elif link_word in self.__cpvd:
            #             pass
            #         elif link_word in self.__cpvi:
            #             pass
            #         else:
            #             continue

            # if target_restriction is not None:
            #     if triple in target_restriction:
            #         continue

            if len(link_word) == 0:
                unclassified_triples.append(triple)
                continue

            # First stage: extracting CSC relations
            if self.__is_csc_relation(first_concept, link_word, second_concept):
                # first concept is subclass of second concept
                self.__owl_encoder.add_csc_relation(class_name=second_concept, subclass_name=first_concept)

            # Second stage: extracting CI relations
            elif link_word in self.__ci:
                # second concept is an instance of first concept
                self.__owl_encoder.add_ci_relation(concept_name=first_concept, instance=second_concept)
            else:
                # Third stage: Extract CP, CPVD, CPVI relations
                if link_word in self.__cp:
                    # second concept is an property of first concept
                    self.__owl_encoder.add_cp_relation(concept_name=first_concept, property_name=second_concept)
                elif self.__is_cpvd_relation(first_concept, link_word, second_concept):
                    # first concept has an direct property - link_word with value - second concept
                    self.__owl_encoder.add_cpvd_relation(first_concept, link_word, second_concept)
                elif link_word in self.__cpvi:
                    # first concept has an indirect property - link_word with value - second concept
                    self.__owl_encoder.add_cpvi_relation(first_concept, link_word, second_concept)
                else:
                    # using WordNet to determine semantic relation between concepts

                    # Translate concepts from 'ru' to 'en' to be able to use nltk.wordnet
                    tr_first = self.__translator.translae(first_concept)
                    tr_second = self.__translator.translae(second_concept)

                    # If YandexTranslate is not available
                    if tr_first == 'ERR_SERVICE_NOT_AVAILABLE' or tr_second == 'ERR_SERVICE_NOT_AVAILABLE':
                        unclassified_triples.append(triple)
                        continue

                    tr_first = tr_first.replace(' ', '_')
                    tr_second = tr_second.replace(' ', '_')

                    s1 = wordnet.synsets(tr_first)
                    s2 = wordnet.synsets(tr_second)

                    # If synsets were not found - continue
                    if len(s1) == 0 or len(s2) == 0:
                        unclassified_triples.append(triple)
                        continue

                    c1_meronyms = []
                    c2_holonyms = []

                    for synset in s1:
                        if synset.pos() == 'n':
                            c1_meronyms.append(synset.part_meronyms())

                    for synset in s2:
                        c2_holonyms.append(synset.part_holonyms())

                    first_match = False

                    for item in c1_meronyms:
                        for meronym in item:
                            for word_form in meronym.lemma_names():
                                if word_form.find(tr_second.lower()) > -1:
                                    first_match = True
                                    break

                    second_match = False

                    for item in c2_holonyms:
                        for holonym in item:
                            for word_form in holonym.lemma_names():
                                if word_form.find(tr_first.lower()) > -1:
                                    second_match = True
                                    break

                    if first_match or second_match:
                        # first concept has an direct property - link_word with value - second concept
                        self.__owl_encoder.add_cpvd_relation(first_concept, link_word, second_concept)
                    else:
                        unclassified_triples.append(triple)

        # unclassified triples
        if len(unclassified_triples) > 0:
            w = RelationsCompletionDialog(triples=unclassified_triples)
            result = w.exec_()

            if result == 1:
                triples = w.relations()

                for triple in triples['CSC']:
                    self.__owl_encoder.add_csc_relation(class_name=triple[2], subclass_name=triple[0])

                for triple in triples['CI']:
                    self.__owl_encoder.add_ci_relation(concept_name=triple[0], instance=triple[2])

                for triple in triples['CP']:
                    self.__owl_encoder.add_cp_relation(concept_name=triple[0], property_name=triple[2])

                for triple in triples['CPVD']:
                    self.__owl_encoder.add_cpvd_relation(triple[0], triple[1], triple[2])

                for triple in triples['CPVI']:
                    self.__owl_encoder.add_cpvi_relation(triple[0], triple[1], triple[2])

            # TODO: исключать тройки, относящиеся к union или restriction из повторной обработки
            # TODO: чтобы не возникло ситуации, когда одна тройка обрабатывалась несколько раз
            # TODO: https://github.com/dveselov/python-yandex-translate - Yandex Translate

    def to_file(self, filename):
        self.__owl_encoder.save_to_file(filename)
