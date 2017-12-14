from textblob import TextBlob

s = raw_input(">>> ")
query = ""

pos_list = ['yes','good','best','love','lucky', 'safe', 'better', 'rich', 'above', 'excellent', 'great', 'success']
neg_list = ['no','bad','worst','hate','unlucky', 'dangerous', 'worse', 'poor', 'below', 'par' , 'small', 'failure']

pos_list_2 = ['is']
neg_list_2 = ['is  not']


def replace_all(text, dic):
    new_text = text
    for i, j in dic.iteritems():
        new_text = new_text.replace(i, j)
    return new_text

replace_pos_sentiment = dict(zip(pos_list,neg_list))
replace_neg_sentiment = dict(zip(neg_list,pos_list))
replace_pos_sentiment_2 = dict(zip(pos_list_2, neg_list_2))
replace_neg_sentiment_2 = dict(zip(neg_list_2, pos_list_2))

sentiment = 'na'
while sentiment=='.':
    p = TextBlob(s).sentiment.polarity
    print p
    if p>0:
        sentiment='pos'
    elif p<0:
        sentiment='neg'
    else:
        print "Could not perceive your stand. Please be clearly FOR or AGAINST the topic"
        sentiment = 'na'
        s = raw_input(">>>")

print sentiment
flag = 0
if(sentiment=='pos'):
    query = replace_all(s, replace_pos_sentiment)
    flag = 1
elif sentiment=='neg':
    query = replace_all(s, replace_neg_sentiment)
    flag = 1

print query