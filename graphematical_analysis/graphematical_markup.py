from xml.dom.minidom import Document
from common.e_label import Grapheme, Label


# Graphematic markup, based on HTML
class GraphematicalMarkup:
    def __init__(self):
        # minidom.Document, converted to plain text
        self.__doc = None

        # tokens styles
        self.__stylesheet = """
                *, body, div {
                    user-select: none;
                    //font-family: Courier New;
                    -webkit-user-select: none;
                }

                .token {
                    height: 18px;
                    max-width: 160px;
                    overflow: hidden;
                    white-space: nowrap;
                    text-overflow: ellipsis;
                    vertical-align: middle;
                    display: inline-block;
                    padding: 1px 5px;
                    border-radius: 3px;
                    margin: 2px;
                    background: #ECECEC;
                    cursor: default;
                }

                /* Simple tokens */
                .token-CYRIL, .token-WORD, .morph-ADJF {
                    background: #FFBFBF;
                }

                .token-LATIN, .token-MIXED, .morph-ADJS {
                    background: #FF8686;
                }

                .token-PUNCT, .morph-VERB {
                    background: #B1BEFF;
                }

                .token-NUMBER, .morph-NOUN {
                    background: #A1EF82;;
                }

                .token-SPACE {
                    background: #ECECEC;
                }

                .token-OTHER {
                    background: #9E9E9E;
                    color: #FFF;
                }

                .token-LINK, .morph-INFN {
                    background: #1E1AFF;
                    color: #FFF;
                }

                .token-EMAIL, .morph-PRTF {
                    background: #13B5DA;
                    color: #FFF;
                }

                .morph-PRTS {
                    background: #0784a0;
                    color: #FFF;
                }

                .token-HASHTAG, .morph-GRND {
                    background: #9C2FFF;
                    color: #FFF;
                }

                .token-MARKUP, .morph-NUMR, token-QUOTE {
                    background: #2D9812;
                    color: #FFF;
                }

                .token-TAG, .morph-PREP {
                    background: #F79F00;
                    color: #FFF;
                }

                .token-CONTENT, .morph-CONJ {
                    background: #BFBF00;
                    color: #FFF;
                }

                .morph-COMP {
                    background: #ce5974;
                    color: #FFF;
                }

                .morph-ADVB {
                    background: #64edd4;
                }

                .morph-NPRO {
                    background: #97de49;
                }

                .morph-PRED {
                    background: #a93f92;
                    color: #FFF;
                }

                .morph-PRCL {
                    background: #fbeb2b;
                }

                .morph-INTJ {
                    background: #ff7818;
                    color: #FFF;
                }

                .morph-LATN {
                    background: #333;
                    color: #FFF;
                }

                .parse > div {
                    background: #fafafa;
                    color: #666;
                    border: 1px solid #e5e5e5;
                    border-radius: 4px;
                    border-bottom: none;
                }
                """

        # xml-root
        self.__root = Document()

        # creating <html><head><style> ... </style></head></html>
        self.__schema = self.__root.createElement('html')
        self.__root.appendChild(self.__schema)

        head = self.__root.createElement('head')
        style = self.__root.createElement('style')
        style_text = self.__root.createTextNode(self.__stylesheet)
        style.appendChild(style_text)

        head.appendChild(style)
        self.__schema.appendChild(head)

        # creating <body></body> element
        self.__body = self.__root.createElement('body')
        self.__schema.appendChild(self.__body)

        # div, which contains all of tokens
        self.__div = self.__root.createElement('div')
        self.__body.appendChild(self.__div)

    def generate_from_tokens(self, tokens):
        for token in tokens:
            self.add_token(token)

    def add_token(self, token):
        # creating <span></span> element
        span = self.__root.createElement('span')
        span_text = self.__root.createTextNode(token.get_text())
        span.appendChild(span_text)

        # adding span attributes
        span_class = "token "
        span_title = []

        for label in token.get_labels():
            if label == Label.WORD:
                span_class += " token-WORD"
                span_title.append("WORD")

            if label == Label.QUOTE:
                span_class += " token-QUOTE"
                span_title.append("QUOTE")

            if label == Label.NUMBER:
                span_class += " token-NUMBER"

            if label == Label.SPACE:
                span_class += " token-SPACE"

            if label == Label.LINK:
                span_class += " token-LINK"

            if label == Label.EMAIL:
                span_class += " token-EMAIL"

            if label == Label.HASHTAG:
                span_class += " token-HASHTAG"

            if label == Label.CYRIL:
                span_class += " token-CYRIL"
                span_title.append("CYRIL")

            if label == Label.LATIN:
                span_class += " token-LATIN"
                span_title.append("LATIN")

            if label == Label.PUNCT:
                span_class += " token-PUNCT"

            if label == Label.MARKUP:
                span_class += " token-MARKUP"
                span_title.append("MARKUP")

            if label == Label.OPENING:
                span_title.append("OPENING")
            elif label == Label.CLOSING:
                span_title.append("CLOSING")

            if label == Label.OTHER:
                span_class += " token-OTHER"

        span.setAttribute('class', span_class)
        span.setAttribute('title', ", ".join(span_title))

        # append span
        self.__div.appendChild(span)

    def get_document(self):
        # Build doc

        self.__doc = str(self.__root.toprettyxml(indent="  "))
        self.__doc = self.__doc.replace('<?xml version="1.0" ?>', '<!DOCTYPE html>')

        return self.__doc
