from similarity import symmetric_sentence_similarity
from pattern.web import plaintext

def get_array(sentences, raw_query, work_range, similarity_threshold_max):
    reply_unsorted = []
    reply_sorted = []
    sort_linker = {}
    sort_values = []
    index = 0
    for sentence in sentences[work_range['start']:work_range['end']]:
        similarity_value = symmetric_sentence_similarity(sentence, raw_query)
        # if similarity_value > similarity_threshold_max:
        sort_values.append(similarity_value)
        # try:    # remove because it holds meaning no more.
        reply_unsorted.append(sentence.encode('utf-8'))  # old
        sort_linker[similarity_value] = sentence.encode('utf-8') # old
            # reply_unsorted.append(plaintext(sentence).encode('utf-8'))  # old
            # sort_linker[similarity_value] = plaintext(sentence).encode('utf-8') # old
            # reply_unsorted.append(str(plaintext(sentence)))   # oldest
            # sort_linker[similarity_value] = str(plaintext(sentence))  # oldest
        # except (UnicodeDecodeError, UnicodeEncodeError):
        #     reply_unsorted.append(plaintext(sentence).encode('utf-8'))
        #     sort_linker[similarity_value] = plaintext(sentence).encode('utf-8')
        # finally:
        index += 1

    sort_values = sorted(sort_values, reverse=False) # alternatively sort_values.sort()
    sort_values = [sort_linker[index] for index in sort_values]
    # reply_sorted = [sort_linker[index] for index in sort_values]
    similarity_threshold_mid = similarity_threshold_max - 0.1
    similarity_threshold_min = similarity_threshold_max - 0.2
    def return_match(value, array):
        index = 0
        for element in array:
            if value >= element:
                break
        return index

    if '' in sort_values:
        sort_values.remove('')
    match_quality = 'H'
    index = [return_match(similarity_threshold_max, sort_values) for value in sort_values]
    print 'Flag 1'
    if index>=3:
        reply_sorted = sort_values[0:3]
    elif index<3:
        print 'Flag 2'
        match_quality = 'M'
        index = [return_match(similarity_threshold_mid, sort_values) for value in sort_values]
        if index>=3:
            reply_sorted = sort_values[0:3]
        elif index<3:
            print 'Flag 3'
            match_quality = 'L'
            index = [return_match(similarity_threshold_min, sort_values) for value in sort_values]
            if index>=3:
                reply_sorted = sort_values[0:3]
            elif index<3:
                print 'Flag 4'
                match_quality = 'NA'
                reply_sorted = sort_values[0:index]

    # print '\nGet Relevant: ', reply_sorted
    return reply_sorted, match_quality
