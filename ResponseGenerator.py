from textblob import TextBlob, Sentence, Word
from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
import MBSP

#Helper method
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def queryGenerator():
    #
    #Step 1: Obtain input from the user
    #
    s = raw_input(">>> ")

    #
    #Step 2: Convert the sentence into blob and MBSP Sentence objects respectively
    #
    input_string = TextBlob(s)
    clipsSentence = MBSP.Sentence(MBSP.parse(s), token=[MBSP.WORD,MBSP.POS,MBSP.CHUNK,MBSP.PNP,MBSP.REL,MBSP.ANCHOR,MBSP.LEMMA])

    #
    #Step 3: Define the variable required for the analysis and interpretation of input
    #
    query = ""
    w = []
    subjPhrases, verbPhrases, predPhrases = [],[],[]
    pNouns, verbs = [],[]
    pnps, anchors = [], []

    #
    #Step 4: Obtain all the proper nouns from the sentence
    #
    for sentence in input_string.sentences:
        tagged = sentence.tags
        for word_tag in tagged:
            if word_tag[1]=='NNP' or word_tag[1]=='NNPS':
                pNouns.append(word_tag[0])
        
    #
    #Step 5: Obtain the different parts, i.e. subject, predicate, object of the sentence
    #
    for chunk in clipsSentence.chunks:
        if chunk.role == 'SBJ' and chunk not in subjPhrases:
            subjPhrases.append(chunk.string)
        elif (chunk.type == 'VP' or chunk.type == 'ADVP') and chunk not in verbPhrases:
            verbPhrases.append(chunk.string)
        elif (chunk.role == 'PRD' or chunk.role == 'OBJ') and chunk not in predPhrases:
            predPhrases.append(chunk.string)

    #
    #Step 6: Detect the noun phrase and the anchors corresponding to them(Ref:CLIPS docs)
    #
    pnps = clipsSentence.pnp
    for np in pnps:
        if np.anchor not in anchors:
            anchors.append(np.anchor)

    #
    #Step 7.1: Build a short relevant query based on available information
    #
    #Note:make priority lists for different set of words
    lines = open('replace_list.csv', 'r').readlines()
    replace_dict = {}
    for line in lines:
        kv = line.split(',')
        replace_dict[kv[0]] = kv[1]
    #
    #Step 7.2: Train the classifier for sentiment data
    #
    ###with open('sentiment_training_formatted.csv', 'r') as fp:
    ###    classifier = NaiveBayesClassifier(fp, format='csv')

    #
    #Step 7.3: Classify the user input and record the sentiment
    #
    def getSentiment(sentence):
        sentiObj= TextBlob(s, analyzer=NaiveBayesAnalyzer()).sentiment
        pos_ratio = sentiObj.p_pos
        neg_ratio = sentiObj.p_neg
        if pos_ratio>=neg_ratio:
            return 'pos'
        else:
            return 'neg'

    input_sentiment = getSentiment(input_string)

    #
    #Step 7.4: Replace words from the array and record the sentiment
    #
    def replace_words(phrase):
        new_phrase = replace_all(phrase, replace_dict)
        return new_phrase

    #
    #Step 8: Generate the final query
    #
    for pN in pNouns:
        for sbj in subjPhrases:
            if pN not in subjPhrases:
                query = query+pN+" "
                print 'pN:'+pN

    for sbj in subjPhrases:
        sbj = replace_words(sbj)
        query = query+sbj+" "
        print 'sbj:'+sbj

    for prd in predPhrases:
        prd = replace_words(prd)
        query = query+prd+" "
        print 'prd:'+prd

    for vr in verbPhrases:
        vr = replace_words(vr)
        query = query+vr+" "
        print 'vr:'+vr

    for anc in anchors:
        anc = anc.string
        anc = replace_words(anc)
        query = query+anc+" "
        print 'anc:'+anc

    for pnp in pnps:
        pnp = pnp.string
        pnp = replace_words(pnp)
        query = query+pnp+" "
        print 'pnp:'+pnp

    #
    #Step 9: Filter query for a,an,the,is
    #
    reps = {' a ':' ', ' an ':' ', ' the ':' ', ' is ':' '}
    query = replace_all(query, reps)

    #
    #Step 10: Remove repetitive words from the sentence
    #
    query_blob = TextBlob(query)
    wrds = query_blob.words
    final_words = []
    for wrd in wrds:
        print wrd
        if wrd not in final_words:
            final_words.append(wrd)

    final_query = ""
    for wrd in final_words:
        final_query = final_query+wrd+" "

    #
    #Step 11: Get the sentiment of the final query
    #
    final_query_sentiment = getSentiment(final_query)

    #
    #Step 12: Print out the query
    #
    print "<------------------------------------------->"
    print "in:",s,"|sentiment:",input_sentiment
    print "out:",final_query,"|sentiment:",final_query_sentiment
    print "<------------------------------------------->"

    return final_query

queryGenerator()