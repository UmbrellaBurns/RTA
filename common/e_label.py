from enum import Enum


class Grapheme(Enum):
    DEL = 1         # Delimiter (разделитель)
    SIG = 2         # Signum (знак препинания/пунктуации)
    RLE = 3         # Russian Lexeme (русская лексема)
    LLE = 4         # Latin Lexeme (лексема на латинице)
    DC = 5          # Digit Complex (цифровой комплекс)
    END = 6         # End of sentence (конец предложения)
    COMPOSITE = 7   # Composite gprapheme (составная графема)
    SYM = 8         # Another single symbols (остальные одиночные символы)


class Label(Enum):
    WORD = 1        # Word (слово)
    NUMBER = 2      # Number (число)
    SPACE = 3       # Space (пробельные символы)
    LINK = 4        # Link (ссылка)
    EMAIL = 5       # Email (электронная почта)
    HASHTAG = 6     # Hashtag (хештег)
    CYRIL = 7       # Cyril (кирилица)
    LATIN = 8       # Latin (латиница)
    PUNCT = 9       # Punctuation marks (знаки пунктуации)
    MARKUP = 10     # Markup symbols (символы разметки)
    QUOTE = 11      # Quote marks (символы цитирования)
    OPENING = 12    # Opening symbol (открывающий символ)
    CLOSING = 13    # Cloing symbol (закрывающий симол)
    OTHER = 14      # All other symbols (все остальные символы)


class Morph(Enum):
    NOUN = 1
    NPRO = 2
    NUMR = 3
    ADJF = 4
    ADJS = 5
    COMP = 6
    VERB = 7
    INFN = 8
    PRTF = 9
    PRTS = 10
    GRND = 11
    ADVB = 12
    PRED = 13
    PREP = 14
    CONJ = 15
    PRCL = 16
    INTJ = 17
    LATN = 18
    OTHER = 19