from similarity import symmetric_sentence_similarity
from pattern.web import plaintext

def get_array(sentences, raw_query):
    reply_unsorted = []
    reply_sorted = []
    sort_linker = {}
    sort_values = []
    matchGoogle = 0.7
    matchTwitter = 0.7
    google_till = int(round(len(sentences)/2))
    index = 0
    for sentence in sentences[1:google_till]:
        similarity_value = symmetric_sentence_similarity(sentence, raw_query)
        if similarity_value > 0.6:
            sort_values.append(similarity_value)
            try:
                reply_unsorted.append(str(plaintext(sentence)))
                sort_linker[similarity_value] = str(plaintext(sentence));
            except (UnicodeDecodeError, UnicodeEncodeError):
                reply_unsorted.append(plaintext(sentence).encode('utf-8'))
                sort_linker[similarity_value] = plaintext(sentence).encode('utf-8');
            finally:
                index += 1

    index1 = 0
    for sentence in sentences[google_till:len(sentences)]:
        similarity_value = symmetric_sentence_similarity(sentence, raw_query)
        if similarity_value > 0.7:
            # sort_linker.append(symmetric_sentence_similarity(sentence, raw_query))
            sort_values.append(similarity_value)
            try:
                reply_unsorted.append(str(plaintext(sentence)))
                sort_linker[similarity_value] = str(plaintext(sentence));
            except (UnicodeDecodeError, UnicodeEncodeError):
                reply_unsorted.append(plaintext(sentence).encode('utf-8'))
                sort_linker[similarity_value] = plaintext(sentence).encode('utf-8');
            finally:
                index1 += 1

    sort_values = sorted(sort_values, reverse=False) # alternatively sort_values.sort()
    reply_sorted = [sort_linker[index] for index in sort_values]
    
    return reply_sorted
