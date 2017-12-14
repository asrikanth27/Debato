from textblob import TextBlob, Word
from textblob.wordnet import VERB
from textblob.np_extractors import ConllExtractor, FastNPExtractor # for noun-phrase chunking
from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
import similarity, datamine, extract_info, np_extractor, json, get_relevant, TextAnalyser
from ast import literal_eval
from pattern.web import plaintext

# Uncomment below to create noun_phrases and actually search for related information
raw_query = raw_input('Enter argument: ')
# search_query_array = extract_info.noun_phrases(raw_query)
search_query = TextAnalyser.queryGenerator(raw_query)
print 'Search Query: ', isinstance(search_query, str)
search_query = str(search_query)

# Mining information
returned_data = datamine.get_info(search_query)
index=-1
for data in returned_data["Result"]:
    index += 1
    try:
        data = data.encode('ascii')
    except (UnicodeEncodeError, UnicodeDecodeError):
        data = data.encode('utf-8')
    finally:
        returned_data["Result"][index] = data
# print '\nMined Data Result: ', returned_data["Result"]

f = open('info.json', 'w')
# f1 = open('info_dummy.txt', 'w')
# f.write(file_write_data)
json.dump(returned_data["Result"], f)
# f1.write(file_write_data1)
f.close()
# f1.close()

# This part calculates similarity within texts
f = open('info.json', 'r+')
# raw_read = f.read()
json_read = json.load(f)
f.close()

sentences = json_read

counters = get_relevant.get_array(sentences, raw_query)

print 'Possible counters: '
index = 0
for line in counters:
    index += 1
    print '\n', str(index), ') ', line
