from pattern.web import asynchronous, time, Google, SEARCH, plaintext, Bing, Twitter, Facebook, Wikipedia, Flickr

def get_info(search_query):
	if isinstance(search_query, str):
		search_query = str(search_query)
	else:
		return { "Error": "Pass a string, from mine.py [7]", "Result": [None] }

	result = []
	engineGoogle = Google(license=None, throttle=0.5, language=None)
	engineBing = Bing(license=None, throttle=0.5, language=None)
	engineTwitter = Twitter(license=None, throttle=0.5, language=None)
	engineFacebook = Facebook(license=None, throttle=1.0, language='en')
	engineWikipedia = Wikipedia(license=None, throttle=5.0, language=None)
	engineFlickr = Flickr(license=None, throttle=5.0, language=None)
	engineArray = [engineGoogle, engineBing, engineTwitter, engineFacebook, engineWikipedia, engineFlickr]
	engineArray = [engineGoogle, engineTwitter]

	'''
	for i in range(1,2):
		# result = result + ([repr(plaintext(para.text)) for para in engine[0].search(search_query, type=SEARCH, start=i, count=5)])
		[result.append([result.append(repr(plaintext(para.text))) for para in engine.search(search_query, type=SEARCH, start=i, count=5)]) for engine in engineArray]
			# print repr(plaintext(para.text))
			# print repr(plaintext(para.url)) + '\n\n'
			# result.append(repr(plaintext(para.text)))
	'''

	# Google
	for i in range(1, 5):
		result = result + ([para.text for para in engineGoogle.search(search_query, type=SEARCH, start=i, count=10)])
		
	for i in range(1, 5):
		result = result + ([para.text for para in engineTwitter.search(search_query, type=SEARCH, start=i, count=10)])
	'''
	# for i in range(1,2):
		# result = result + ([repr(plaintext(para.text)) for para in engineBing.search(search_query, type=SEARCH, start=i, count=5)])
	for i in range(1,2):
		result = result + ([repr(plaintext(para.text)) for para in engineTwitter.search(search_query, type=SEARCH, start=i, count=10)])
	# for i in range(1,2):
		# result = result + ([repr(plaintext(para.text)) for para in engineFacebook.search(search_query, type=SEARCH, start=i, count=5)])
	# for i in range(1,2):
		# result = result + ([repr(plaintext(para.text)) for para in engineWikipedia.search(search_query, type=SEARCH, start=i, count=5)])
	# for i in range(1,2):
		# result = result + ([repr(plaintext(para.text)) for para in engineFlickr.search(search_query, type=SEARCH, start=i, count=5)])
	'''

	return { "Error": None, "Result": result }

	# return { "Error": None, "Result": ['Hello World', 'Bye Bye Tommy'] }