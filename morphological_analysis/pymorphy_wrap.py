import pymorphy2


class MorphAnalyzer:
    class __Morph:
        morph = pymorphy2.MorphAnalyzer()

        def parse(self, string):
            return self.morph.parse(string)

        def get_best_parse_result(self, string):
            target = self.morph.parse(string)

            max_score = target[0].score
            parse_number = 0

            for i in range(1, len(target)):
                if target[i].score > max_score:
                    max_score = target[i].score
                    parse_number = i

            return target[parse_number]

        def lat2cyr(self, grammeme):
            return self.morph.lat2cyr(grammeme)

    __instance = None

    def __init__(self):

        if MorphAnalyzer.__instance is None:
            MorphAnalyzer.__instance = MorphAnalyzer.__Morph()

        self.__dict__['__MorphAnalyzer_instance'] = MorphAnalyzer.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

