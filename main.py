print 'Loading libraries...\n'
import data_mine, json, get_relevant, TextAnalyser, time # , pickle
from cStringIO import StringIO

class conversation_class:
    def __init__(self, user_argument):
        self.user_argument = user_argument
        self.returned_results = []
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
    def addReturnedResults(self, returned_results):
        self.returned_results = self.returned_results + returned_results
        return False

    def printReturnedResults(self):
        print '\nSearch Results: \n'
        index = 0
        for sentence in self.returned_results:
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

def run(take_raw=False):
    # Text Analysis
    if not take_raw:
        raw_query = raw_input('Enter argument: ')
    conversation = conversation_class(raw_query)
    print 'Starting text analysis...\n'
    # search_query_array = extract_info.noun_phrases(raw_query)
    search_query, isMeaning = TextAnalyser.queryGenerator(raw_query, not take_raw)
    search_query = str(search_query)
    conversation.addSearchQuery(search_query)

    if not isMeaning:
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
        conversation.addReturnedResults(returned_data["Result"])
        f = open('info.json', 'w')
        json.dump(returned_data["Result"], f)
        f.close()

        # Calculating similarity within texts
        print 'Generating counters...\n'
        f = open('info.json', 'r+')
        sentences = json.load(f)
        f.close()
        f = open('previous_results.json', 'r+')
        conversation.addPreviousCounters(json.load(f))
        f.close()

        # TODO: combine counters before passing it to get_relevant
        google_range = { 'start': 0, 'end': int(round(len(sentences)/2)) }
        twitter_range = { 'start': int(round(len(sentences)/2)), 'end': len(sentences) }
        counters = get_relevant.get_array(sentences, raw_query, google_range)
        combined = counters
        for x in conversation.previous_counters:
            if x not in counters:
                combined.append(x)

        # combined = counters + conversation.previous_counters
        try:
            counters = get_relevant.get_array(counters, conversation.user_argument, { 'start': 0, 'end': len(conversation.previous_counters) + len(counters) })
        except (UnicodeDecodeError, UnicodeEncodeError):
            combined = [c.encode('utf-8') for c in combined]
            counters = get_relevant.get_array(combined, conversation.user_argument, { 'start': 0, 'end': len(conversation.previous_counters) + len(counters) })
        tweets = get_relevant.get_array(sentences, raw_query, twitter_range)
        conversation.addCounters(counters)
        conversation.addTweets(tweets)

        response_analyzed_string_array = []
        rerun = conversation.printCounters()
        if rerun:
            run(conversation.user_argument)
            return

        f = open('previous_results.json', 'w')
        if len(counters) > 3:
            json.dump(counters[0:3], f)
        else:
            json.dump(counters, f)
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
    return

run()
