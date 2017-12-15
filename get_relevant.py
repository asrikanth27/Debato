from similarity import symmetric_sentence_similarity
from pattern.web import plaintext

def get_array(sentences, raw_query, work_range, similarity_threshold):
    reply_unsorted = []
    reply_sorted = []
    sort_linker = {}
    sort_values = []
    index = 0
    for sentence in sentences[work_range['start']:work_range['end']]:
        similarity_value = symmetric_sentence_similarity(sentence, raw_query)
        if similarity_value > similarity_threshold:
            sort_values.append(similarity_value)
            try:
                reply_unsorted.append(str(plaintext(sentence)))
                sort_linker[similarity_value] = str(plaintext(sentence));
            except (UnicodeDecodeError, UnicodeEncodeError):
                reply_unsorted.append(plaintext(sentence).encode('utf-8'))
                sort_linker[similarity_value] = plaintext(sentence).encode('utf-8');
            finally:
                index += 1

    sort_values = sorted(sort_values, reverse=False) # alternatively sort_values.sort()
    reply_sorted = [sort_linker[index] for index in sort_values]
    
    return reply_sorted
