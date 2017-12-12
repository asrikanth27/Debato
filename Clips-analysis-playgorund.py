import MBSP
from pattern.web import Google, Twitter, plaintext
from pattern.en import parse

s1 = "Narendra Modi is prime minister of India"
s2 = "Mariana Trench is deepest point on earth"
s3 = "Swachh Bharat Abhiyan"
s4 = "I love the taste of this cake!!"
s4 = "The profit in today's business is Rs.52"
s5 = "The share market fell by 12%"
s6 = "Python is a very powerful language"
s7 = "What am I to do with this?"
s8 = "Humpty Dumpty sat on a wall, humpty dumpty had a great fall..."
s9 = "log(1+n) = 1 + 1/2! + 1/3! + .... + 1/n!"
s10 = "Crpytocurrency is safe for investment."

s = s10
#lemmatization -> finds the dictionary or simple form of the word
#MBSP.taginfo() -> give the description of the tags with an optional example
#tokenise.split() -> splits the given text into sentence and/or words

sentence = MBSP.Sentence(MBSP.parse(s), token=[MBSP.WORD,MBSP.POS,MBSP.CHUNK,MBSP.PNP,MBSP.REL,MBSP.ANCHOR,MBSP.LEMMA])

not_word = MBSP.Word("","not", lemma=None, type=None, index=0)
query = ""
for chunk in sentence.chunks:
    if chunk.role == 'SBJ':
        query = query+chunk.string+" "
    if chunk.type == 'VP' or chunk.type == 'ADVP':
        query = query+"not "+chunk.string+" "
    if chunk.role == 'PRD' or chunk.role == 'OBJ':
        query = query+chunk.string+" "
print "????????????????????????????????????"
print query
print "????????????????????????????????????", "\n\n", "RESULTS: \n"
engine = Google(license=None)
results = engine.search(query,start=1, count=10,size=None)
for result in results:
    print plaintext(result.text)
    print "***************************************"
    print MBSP.pprint(parse(result.text, relations = True, lemmata=True))
    print "<<------------------------------------------------------------>>"