from translator.translate import Translator


def learn_translator(tran):

    with open('ru.txt', 'r', encoding='utf-8') as f:
        ru = f.read()

    with open('en.txt', 'r', encoding='utf-8') as f:
        en = f.read()

    ru = ru.split('\n')
    en = en.split('\n')

    if len(ru) == len(en):
        for i in range(0, len(ru)):
            tran.add_word(ru[i], en[i])


if __name__ == '__main__':

    tran = Translator()

    print(tran.translae('шлгшдгщд'))

    print(tran.transliterate("шлгшдгщд"))
