from pattern.en import parsetree
import MBSP

text = 'Automation is good for the economy. A world dominated by robots is a thing I am looking forward to!'
text = raw_input('Enter text: ')

parse_tree = parsetree(text)

for sentence in parse_tree:
	for chunk in sentence.chunks:
		for word in chunk.words:
			print str(word),
		print '\n', str(chunk)
		print

self_parse = []
construct = []
sentence = []
parsed_text = MBSP.parse(text)
parsed_sentences = parsed_text.split('O/.')
parsed_words = parsed_text.split(' ')
for word in parsed_words:
	element = [e.encode('ascii') for e in word.split('/')]
	construct.append(element)
	if element[1]=='.':
		sentence.append(construct)
		construct = []
	print element
print

# print str(parsed_text)
print [word[0] for word in sentence[0]]
