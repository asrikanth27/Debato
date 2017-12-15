print 'Loading libraries...\n'
import data_mine, json, get_relevant, TextAnalyser, time

# Text Analysis
raw_query = raw_input('Enter argument: ')
print 'Starting text analysis...\n'
search_query, isMeaning = TextAnalyser.queryGenerator(raw_query, True)

if not isMeaning:
    print 'Search Query: ', isinstance(search_query, str)
    search_query = str(search_query)

    # Mining information
    print 'Mining information off the web...\n'
    returned_data = data_mine.get_info(search_query)
    index=-1
    for data in returned_data["Result"]:
        index += 1
        try:
            data = data.encode('ascii')
        except (UnicodeEncodeError, UnicodeDecodeError):
            data = data.encode('utf-8')
        finally:
            returned_data["Result"][index] = data

    # Storing the mined information
    print 'Done mining, saving changes...\n'
    f = open('info.json', 'w')
    json.dump(returned_data["Result"], f)
    f.close()

    # Calculating similarity within texts
    print 'Generating counters...\n'
    f = open('info.json', 'r+')
    json_read = json.load(f)
    f.close()

    sentences = json_read

    google_range = { 'start': 0, 'end': int(round(len(sentences)/2)) }
    twitter_range = { 'start': int(round(len(sentences)/2)), 'end': len(sentences) }
    counters = get_relevant.get_array(sentences, raw_query, google_range)
    tweets = get_relevant.get_array(sentences, raw_query, twitter_range)

    response_analyzed_string_array = []
    print 'Search results: \n'
    index = 0
    for sentence in sentences:
        index += 1
        print '\n', str(index), ') ', sentence

    print 'Possible counters: \n'
    if len(counters)>=3:
        print '',
        # counter_save = counters[0]
        # counters[0:2] = counters[1:3]
        # counters[2] = counter_save
    else:
        print '\nProbably you are right! WOW!'
    index = 0
    for line in counters:
        index += 1
        print '\n', str(index), ') ', line
        if index==3:
            break
    index = 0
    for line in tweets:
        index += 1
        print '\n', str(index), ') ', line

else:
    print search_query

print '\n\n Done:)'
