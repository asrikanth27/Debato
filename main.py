print 'Loading libraries...\n'
import data_mine, json, get_relevant, TextAnalyser, time # , pickle
from pattern.web import plaintext
from cStringIO import StringIO

class conversation_class:
    def __init__(self, user_argument):
        self.user_argument = user_argument
        self.mined_data = {}
        self.counters = []
        self.tweets = []
        self.previous_counters = []
        self.search_query = ''

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
            print '\n', str(index), ') ', line
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

def run(input_string,take_raw=False):
    # Text Analysis ----------------------------------------------------------------------------
    #if not take_raw:
    #   raw_query = raw_input('Enter argument: ')
    raw_query = input_string
    conversation = conversation_class(raw_query)
    print 'Starting text analysis...\n'
    # search_query_array = extract_info.noun_phrases(raw_query)
    search_query, isMeaning = TextAnalyser.queryGenerator(raw_query, not take_raw)
    search_query = str(search_query)
    conversation.addSearchQuery(search_query)

    # If user doesn't ask for meaning ----------------------------------------------------------
    if not isMeaning:
        # Mining information -------------------------------------------------------------------
        print 'Mining information off the web...\n'
        mined_data = data_mine.get_info(search_query)
        if mined_data['Error']:
            print mined_data['Error']
            return None
        # Encode mined data for further use
        for engine in ['Google', 'Twitter']:
            index=0
            for data in mined_data[engine]:
                try:
                    data['text'] = data['text'].encode('ascii')
                    data['url'] = data['url'].encode('ascii')
                    data['title'] = data['title'].encode('ascii')
                    # data['url'] = [data_single.encode('ascii') for data_single in data['url']]
                    # data['title'] = [data_single.encode('ascii') for data_single in data['title']]
                except (UnicodeEncodeError, UnicodeDecodeError):
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
            'Google': 0.6,
            'Twitter': 0.5
        }
        try:
            google_counters = get_relevant.get_array(google_text, conversation.user_argument, google_range, similarity_threshold['Google'])
        except (UnicodeDecodeError, UnicodeEncodeError):
            print '\nUnicode exception at google_counters(similarity) !, trying utf-8 encoding'
            google_text = [iterator.encode('utf-8') for iterator in combined]
            google_counters = get_relevant.get_array(google_text, conversation.user_argument, twitter_range, similarity_threshold['Google'])
        try:
            twitter_counters = get_relevant.get_array(twitter_text, conversation.user_argument, google_range, similarity_threshold['Twitter'])
        except (UnicodeDecodeError, UnicodeEncodeError):
            print '\nUnicode exception at twtter_counters(similarity) !, trying utf-8 encoding'
            twitter_text = [iterator.encode('utf-8') for iterator in combined]
            twitter_counters = get_relevant.get_array(twitter_text, conversation.user_argument, twitter_range, similarity_threshold['Twitter'])
        # tweets = get_relevant.get_array(sentences, raw_query, twitter_range)
        conversation.addCounters(google_counters)
        conversation.addTweets(twitter_counters)

        response_analyzed_string_array = []
        rerun = conversation.printCounters()
        if rerun:
            print '\nRerunning as counters not up to the mark!'
            run(conversation.user_argument)
            return

        f = open('previous_results.json', 'w')
        if len(google_counters) > 3:
            google_counters_array = []
            index = 0
            for google in conversation.mined_data['Google']:
                for counter_text in google_counters:
                    if plaintext(google['text']).encode('utf-8') ==  counter_text:
                        google_counters_array.append(google)
                        index += 1
                    if index>=3:
                        break

            json.dump(google_counters_array, f)
        else:
            google_counters_array = []
            for google in conversation.mined_data['Google']:
                for counter_text in google_counters:
                    if plaintext(google['text']).encode('utf-8') ==  counter_text:
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

    print '\n\nDone:)'
    return conversation.counters