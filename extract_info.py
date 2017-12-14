from textblob import TextBlob, Word
from textblob.wordnet import VERB
from textblob.np_extractors import ConllExtractor, FastNPExtractor # for noun-phrase chunking

def noun_phrases(query):
	# noun-phrase chunking
	# extractor = FastNPExtractor()
	extractor = ConllExtractor()
	blob = TextBlob(query, np_extractor=extractor)
	noun_phrases = blob.noun_phrases
	return noun_phrases
