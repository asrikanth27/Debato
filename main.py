print 'Loading libraries...\n'
import data_mine, json, get_relevant, TextAnalyser, time, sentence_similarity # , pickle
from pattern.web import plaintext

print 'Whenever you are ready ... '

class conversation_class:
    def __init__(self, user_argument):
        self.user_argument = user_argument
        self.mined_data = {}
        self.counters = []
        self.tweets = []
        self.previous_counters = []
        self.search_query = ''
        self.result = {}

    def addCounters(self, counters):
        self.counters = self.counters + counters
        return False
    def addTweets(self, tweets):
        self.tweets = self.tweets + tweets
        return False
    def addPreviousCounters(self, previous_counters):
        self.previous_counters = self.previous_counters + previous_counters
        return False
    def addSearchQuery(self, search_query):
        self.search_query = search_query
        return False
    def addReturnedResults(self, mined_data):
        self.mined_data = mined_data
        return False

    def printReturnedResults(self):
        print '\nSearch Results: \n'
        index = 0
        for sentence in self.mined_data:
            index += 1
            print '\n', str(index), ') ', sentence
        return False
    def printCounters(self):
        print 'Counters: \n'
        if len(self.counters)==0:
            print '\nProbably you are right! WOW!'
            return True
        index = 0
        for line in self.counters:
            index += 1
            print '\n', str(index), ') ', line.replace('\n', ' ')
            if index==3:
                break
        return False
    def printTweets(self):
        print '\nTweets: \n'
        index = 0
        for line in self.tweets:
            index += 1
            print '\n', str(index), ') ', line
        return False

    def resultFormer(self, google, twitter):
        # print '\nGoogle: ', google, '\nTwitter: ', twitter, '\nMined Data: ', self.mined_data
        result_google = []
        for string in google:
            for data in self.mined_data['Google']:
                if data['text'].encode('utf-8')==string:
                    result_google.append({ 'url': plaintext(data['url']).encode('utf-8'), 'title': plaintext(data['title']).encode('utf-8'), 'text': plaintext(data['text']).encode('utf-8') })
        result_twitter = []
        for string in twitter:
            for data in self.mined_data['Twitter']:
                if data['text'].encode('utf-8')==string:
                    result_twitter.append({ 'url': plaintext(data['url']).encode('utf-8'), 'title': plaintext(data['title']).encode('utf-8'), 'text': plaintext(data['text']).encode('utf-8') })

        self.result = { 'Error': None, 'Google': result_google, 'Twitter': result_twitter }
        return self.result

def check_single_sentence(query):
    temp = query.split('.')
    if '' in temp:
        temp.remove('')
    return len(temp) < 2

def remove_duplicate(passed_list):
    unique = []
    for element in passed_list:
        if element not in unique:
            unique.append(element)

    return unique
    
def run_multiple(raw_query, change_sentiment=True, recursing=False):
    # Text Analysis ----------------------------------------------------------------------------
    # if not take_raw:
       # raw_query = raw_input('Enter argument: ')

    # raw_query = raw_query.split('.').remove('')
    print raw_query, ' Multi!!!!!'
    raw_query = raw_query.split('.')
    if '' in raw_query:
        raw_query.remove('')

    multi_mined_data = {
        'Error': None,
        'Google': [],
        'Twitter': []
    }
    for sentence in raw_query:
        mined_data, confidence = run(sentence, change_sentiment=change_sentiment, recursing=True, returnall=True)
        # print 'Within multi: ', counters
        try:
            if len(mined_data['Google'])>0 or not len(mined_data['Google'])==None:
                multi_mined_data['Google'] = multi_mined_data['Google'] + mined_data['Google']
        except TypeError:
            print 'Type Error for: ', sentence
        try:
            if len(mined_data['Twitter'])>0 or not len(mined_data['Twitter'])==None:
                multi_mined_data['Twitter'] = multi_mined_data['Twitter'] + mined_data['Twitter']
        except TypeError:
            print 'Type Error for: ', sentence    

    conversation_multi = conversation_class(''.join(raw_query))
    conversation_multi.addReturnedResults(multi_mined_data)
    raw_query_multi = ''.join(raw_query)
    if '..' in raw_query_multi:
        raw_query_multi.remove('..')
    if '...' in raw_query_multi:
        raw_query_multi.remove('...')
    if '....' in raw_query_multi:
        raw_query_multi.remove('....')
    if '.....' in raw_query_multi:
        raw_query_multi.remove('.....')
    if '......' in raw_query_multi:
        raw_query_multi.remove('......')

    print '\nRaw query multi: ', raw_query_multi
    # return 0

    print 'Combining counters...\n'
    # TODO: combine counters before passing it to get_relevant
    # counters = get_relevant.get_array(sentences, raw_query, google_range)

    google_range = { 'start': 0, 'end': len(conversation_multi.mined_data['Google']) }
    twitter_range = { 'start': 0, 'end': len(conversation_multi.mined_data['Twitter']) }
    google_text = [iterator['text'] for iterator in conversation_multi.mined_data['Google']]
    twitter_text = [iterator['text'] for iterator in conversation_multi.mined_data['Twitter']]
    similarity_threshold = {
        'Google': 0.2,
        'Twitter': 0.1
    }
    try:
        google_counters = get_relevant.get_array(google_text, conversation_multi.user_argument, google_range, similarity_threshold['Google'])
    except (UnicodeDecodeError, UnicodeEncodeError):
        print '\nUnicode exception at google_counters(similarity) !, trying utf-8 encoding'
        def force_to_unicode(text):
            return text if isinstance(text, unicode) else text.decode('utf8')
        google_text = [force_to_unicode(iterator) for iterator in google_text]
        google_counters = get_relevant.get_array(google_text, conversation_multi.user_argument, google_range, similarity_threshold['Google'])
    try:
        twitter_counters = get_relevant.get_array(twitter_text, conversation_multi.user_argument, twitter_range, similarity_threshold['Twitter'])
    except (UnicodeDecodeError, UnicodeEncodeError):
        print '\nUnicode exception at twtter_counters(similarity) !, trying utf-8 encoding'
        def force_to_unicode(text):
            return text if isinstance(text, unicode) else text.decode('utf8')
        twitter_text = [force_to_unicode(iterator) for iterator in twitter_text]
        twitter_counters = get_relevant.get_array(twitter_text, conversation_multi.user_argument, twitter_range, similarity_threshold['Twitter'])
    conversation_multi.addCounters(google_counters)
    conversation_multi.addTweets(twitter_counters)

    conversation_multi.counters = remove_duplicate(conversation_multi.counters)
    google_counters = conversation_multi.counters

    rerun = conversation_multi.printCounters()
    # if rerun and not recursing:
        # print '\nRerunning as counters not up to the mark!'
        # run(conversation.user_argument, change_sentiment=False, recursing=True)   # put return here!
        # return

    f = open('previous_results.json', 'w')
    if len(google_counters) > 3:
        google_counters_array = []
        index = 0
        for google in conversation_multi.mined_data['Google']:
            for counter_text in google_counters:
                # if plaintext(google['text']).encode('utf-8') ==  counter_text:
                if plaintext(google['text']) ==  counter_text: # replaced from above
                    google_counters_array.append(google)
                    index += 1
                if index>=3:
                    break

        json.dump(google_counters_array, f)
    else:
        google_counters_array = []
        for google in conversation_multi.mined_data['Google']:
            for counter_text in google_counters:
                # if plaintext(google['text']).encode('utf-8') ==  counter_text:
                if plaintext(google['text']).encode('utf-8') ==  counter_text:  # replaced from above
                    google_counters_array.append(google)

        json.dump(google_counters_array, f)
    f.close()

    '''
    f = open('conversation.pkl', 'w')
    src = StringIO()
    p = pickle.Pickler(src)
    # pickle.dump(conversation, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    '''

    print '\n\nDone:)'
    if len(conversation_multi.counters)<=3:
        return conversation_multi.counters
    else:
        return conversation_multi.counters[0:3]

def run(raw_query, change_sentiment=True, recursing=False, returnall=False):
    # Text Analysis ----------------------------------------------------------------------------
    # if not take_raw:
       # raw_query = raw_input('Enter argument: ')

    print raw_query

    if check_single_sentence(raw_query)==False:
        return run_multiple(raw_query, change_sentiment=change_sentiment, recursing=recursing)
    
    conversation = conversation_class(raw_query)
    print 'Starting text analysis...\n'
    if not change_sentiment:
        isMeaning = False
        search_query = str(raw_query)
    else:
        search_query, isMeaning = TextAnalyser.queryGenerator(raw_query, change_sentiment)
    # search_query, isMeaning = 'Modi bad minister', False
    search_query = str(search_query)
    # print '\nSearch query: ', search_query
    conversation.addSearchQuery(search_query)

    # If user doesn't ask for meaning ----------------------------------------------------------
    if not isMeaning:
        # Mining information -------------------------------------------------------------------
        print 'Mining information off the web...\n'
        mined_data = data_mine.get_info(search_query)
        fresh_mined_data = {'Google': [], 'Twitter': [], 'Error': None}
        for fields in mined_data:
            if not fields=='Error':
                for data in mined_data[fields]:
                    if not ''==data['text']:
                        fresh_mined_data[fields].append(data)

        fresh_mined_data['Error'] = mined_data['Error']
        mined_data = fresh_mined_data
        # print '\nMined Data line 246: ', mined_data
        if mined_data['Error']:
            print mined_data['Error']
            return None
        # Encode mined data for further use
        for engine in ['Google', 'Twitter']:
            index=0
            for data in mined_data[engine]:
                try:
                    data['text'] = data['text']
                    data['url'] = data['url']
                    data['title'] = data['title']
                    # data['text'] = data['text'].encode('utf-8')
                    # data['url'] = data['url'].encode('utf-8')
                    # data['title'] = data['title'].encode('utf-8')
                    # data['text'] = data['text'].encode('ascii')
                    # data['url'] = data['url'].encode('ascii')
                    # data['title'] = data['title'].encode('ascii')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    print '\nEncode error at information mining 257...'
                    data['text'] = data['text'].encode('utf-8')
                    data['url'] = data['url'].encode('utf-8')
                    data['title'] = data['title'].encode('utf-8')
                    # data['text'] = [data_single.encode('utf-8') for data_single in data['text']]
                    # data['url'] = [data_single.encode('utf-8') for data_single in data['url']]
                    # data['title'] = [data_single.encode('utf-8') for data_single in data['title']]
                finally:
                    mined_data[engine][index] = data
                index += 1

        # Storing the mined information ---------------------------------------------------------
        print 'Done mining, saving/retrieving changes...\n'
        conversation.addReturnedResults(mined_data)
        fG = open('google_results.json', 'w')
        fT = open('twitter_results.json', 'w')
        json.dump(mined_data["Google"], fG)
        json.dump(mined_data["Twitter"], fT)
        fG.close()
        fT.close()

        # Opening the mined information ---------------------------------------------------------
        fG = open('google_results.json', 'r+')
        fT = open('twitter_results.json', 'r+')
        # sentences = json.load(fG)
        google_results = json.load(fG)
        twitter_results = json.load(fT)
        fG.close()
        fT.close()
        f = open('previous_results.json', 'r+')
        try:
            conversation.addPreviousCounters(json.load(f))
        except (ValueError):
            conversation.addPreviousCounters([])
        f.close()

        # Calculating similarity within texts ---------------------------------------------------
        print 'Generating counters...\n'
        # TODO: combine counters before passing it to get_relevant
        # counters = get_relevant.get_array(sentences, raw_query, google_range)
        for x in conversation.previous_counters:
            if x not in conversation.mined_data['Google']:
                conversation.mined_data['Google'].append(x)

        google_range = { 'start': 0, 'end': len(conversation.mined_data['Google']) }
        twitter_range = { 'start': 0, 'end': len(conversation.mined_data['Twitter']) }
        # combined = counters + conversation.previous_counters
        # print '\nConversation mined data: ', conversation.mined_data
        # print '\nMined data: ', mined_data
        google_text = [iterator['text'] for iterator in conversation.mined_data['Google']]
        twitter_text = [iterator['text'] for iterator in conversation.mined_data['Twitter']]
        similarity_threshold = {
            'Google': 0.7,
            'Twitter': 0.5
        }
        try:
            google_counters, match_quality_google = get_relevant.get_array(google_text, conversation.user_argument, google_range, similarity_threshold['Google'])
        except (UnicodeDecodeError, UnicodeEncodeError):
            print '\nUnicode exception at google_counters(similarity) !, trying utf-8 encoding'
            def force_to_unicode(text):
                return text if isinstance(text, unicode) else text.decode('utf8')
            google_text = [force_to_unicode(iterator) for iterator in google_text]
            google_counters, match_quality_google = get_relevant.get_array(google_text, conversation.user_argument, google_range, similarity_threshold['Google'])
        try:
            twitter_counters, match_quality_twitter  = get_relevant.get_array(twitter_text, conversation.user_argument, twitter_range, similarity_threshold['Twitter'])
        except (UnicodeDecodeError, UnicodeEncodeError):
            print '\nUnicode exception at twtter_counters(similarity) !, trying utf-8 encoding'
            def force_to_unicode(text):
                return text if isinstance(text, unicode) else text.decode('utf8')
            twitter_text = [force_to_unicode(iterator) for iterator in twitter_text]
            twitter_counters, match_quality_twitter = get_relevant.get_array(twitter_text, conversation.user_argument, twitter_range, similarity_threshold['Twitter'])
        conversation.addCounters(google_counters)
        conversation.addTweets(twitter_counters)
        if match_quality_google=='H':
            confidence = 'high confidence'
        elif match_quality_google=='M':
            confidence = 'medium confidence'
        elif match_quality_google=='L':
            confidence = 'low confidence'
        else:
            confidence = 'You are probably right, the results may not be relevant!'

        conversation.counters = remove_duplicate(conversation.counters)
        google_counters = conversation.counters

        print '\nPassing google_counters to get_array'
        efficient_sentences = sentence_similarity.get_sentences(google_counters, raw_query)
        rerun = conversation.printCounters()
        # if rerun and not recursing:
        #     print '\nRerunning as counters not up to the mark!'
        #     return run(conversation.user_argument, change_sentiment=False, recursing=True)
            # return

        f = open('previous_results.json', 'w')
        if len(google_counters) > 3:
            google_counters_array = []
            index = 0
            for google in conversation.mined_data['Google']:
                for counter_text in google_counters:
                    # if plaintext(google['text']).encode('utf-8') ==  counter_text:
                    if plaintext(google['text']) ==  counter_text:  # replaced from above
                        google_counters_array.append(google)
                        index += 1
                    if index>=3:
                        break

            json.dump(google_counters_array, f)
        else:
            google_counters_array = []
            for google in conversation.mined_data['Google']:
                for counter_text in google_counters:
                    # if plaintext(google['text']).encode('utf-8') ==  counter_text:
                    if plaintext(google['text']) ==  counter_text:  # replaced from above
                        google_counters_array.append(google)

            json.dump(google_counters_array, f)
        f.close()

        '''
        f = open('conversation.pkl', 'w')
        src = StringIO()
        p = pickle.Pickler(src)
        # pickle.dump(conversation, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        '''
    else:
        print search_query
        confidence = ''
        title = 'Meaning of: ' + str(raw_query)
        return {'Google': [{'url': '', 'text': search_query, 'title': title}], 'Twitter': [], 'Error': None}, ''

    print '\n\nDone:)'

    return_result = conversation.resultFormer(conversation.counters, conversation.tweets)
    def covert_points(sentence):
        return plaintext(sentence).encode('utf-8') + ' -ang- '
    efficient_sentences = [covert_points(sentence) for sentence in efficient_sentences]
    return_result['Google'].append({'url': 'self url', 'text': ''.join(efficient_sentences), 'title': 'self title'})
    print '\nReturn Result: ', return_result

    if returnall==False:
        if len(conversation.counters)<=3:
            return return_result, confidence
            # return {'Google': conversation.counters, 'Twitter': conversation.tweets, 'Error': None}
        else:
            return return_result, confidence
            # return {'Google': conversation.counters[0:3], 'Twitter': conversation.tweets, 'Error': None}
    else:
        return conversation.mined_data
        