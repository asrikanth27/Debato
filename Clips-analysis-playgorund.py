import MBSP
from pattern.web import Google, Twitter, plaintext
from pattern.en import parse

s1 = "Narendra Modi is the prime minister"
s2 = "Mariana Trench is deepest point on earth"
s3 = "Swachh Bharat Abhiyan"
s4 = "I love the taste of this cake!!"
s4 = "Manners maketh man"
s5 = "The share market is volatile"
s6 = "Python is a very powerful language"
s7 = "Black is a peaceful colour"
s8 = "Humpty Dumpty sat on a wall, humpty dumpty had a great fall..."
s9 = "I love playing the guitar. It is the best instrument"
s10 = "Crpytocurrency is safe for investment."

s = s1
#lemmatization -> finds the dictionary or simple form of the word
#MBSP.taginfo() -> give the description of the tags with an optional example
#tokenise.split() -> splits the given text into sentence and/or words

sentence = MBSP.Sentence(MBSP.parse(s), token=[MBSP.WORD,MBSP.POS,MBSP.CHUNK,MBSP.PNP,MBSP.REL,MBSP.ANCHOR,MBSP.LEMMA])

c = []
for chunk in sentence.chunks:
    c.append(chunk.string)

print c
print "blah "+c[0]