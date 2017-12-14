from textblob import TextBlob, Sentence, Word

from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer

s = "Vivekananda is a role model for many"
wiki = TextBlob(s, analyzer=NaiveBayesAnalyzer()).sentiment
pos = wiki.p_pos

print wiki
print pos