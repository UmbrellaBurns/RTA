from statistical_analysis.statistical import StatisticalAnalysis
import time


def statistical_analysis_test():
    with open("test.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    time_stamp = time.time()

    analyzer = StatisticalAnalysis(text=text)
    analyzer.analysis()

    time_stamp = time.time() - time_stamp

    print("Finished in {} ms".format(time_stamp))
    print("Text category: {}".format(analyzer.get_text_category()))
    semantic_core = analyzer.get_words_frequency(10)

    print("Characters count: {}".format(analyzer.get_characters_count()))
    print("Characters count without spaces: {}".format(analyzer.get_characters_count_without_spaces()))
    print("Words count: {}".format(analyzer.get_words_count()))

    print("Semantic core: ")
    for key in semantic_core.keys():
        out_w = "\tword: {0}".format(key)
        out_f = "| frequency: {0}".format(semantic_core[key])
        print(out_w.ljust(30) + out_f.rjust(0))
