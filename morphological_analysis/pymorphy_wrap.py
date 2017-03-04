import pymorphy2


class MorphAnalyzer:
    class __Morph:
        morph = pymorphy2.MorphAnalyzer()

        def parse(self, string):
            return self.morph.parse(string)

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

