from similarity import symmetric_sentence_similarity
from pattern.web import plaintext
import math

def get_sentences(text, raw_query):
    map_array = {}
    compare_array = []
    for para in text:
        sentences = para.split('.')
        temp = []
        for sentence_temp in sentences:
            if not sentence_temp=='':
                temp.append(sentence_temp)

        sentences = temp
        # print '\nIndividual sentences: ', sentences
        for sentence in sentences:
            similarity_value = symmetric_sentence_similarity(sentence, raw_query)
            compare_array.append(similarity_value)
            map_array[similarity_value] = sentence  #.encode('utf-8')

    compare_array = sorted(compare_array, reverse=True) # alternatively sort_values.sort()
    # print '\nCompare array reverse sorted 1: ', compare_array
    sorted_sentences_array = [map_array[index] for index in compare_array]
    b1 = len(raw_query)
    a1 = [len(x) for x in sorted_sentences_array]
    c1 = compare_array
    for x in range(0, len(c1)):
        c1[x] = c1[x] * ((b1 / a1[x])^2)
    # print c1
    # sorted_sentences_array = [map_array[index] for index in c1]
    # print '\nSorted sentences array 2: ', sorted_sentences_array
    temp = []
    for sentence_temp in sorted_sentences_array:
        if not sentence_temp=='':
            temp.append(sentence_temp)

    sorted_sentences_array = temp
    # print '\nSorted sentences space removed: ', sorted_sentences_array
    return sorted_sentences_array[0:3]
