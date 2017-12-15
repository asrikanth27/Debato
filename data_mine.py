from pattern.web import Google, SEARCH, Twitter	# , plaintext, Bing, Facebook, Wikipedia, Flickr

def get_info(search_query):
	if isinstance(search_query, str):
		search_query = str(search_query)
	else:
		return { "Error": "Pass a string, from mine.py [7]" }

	google = [{
		'text': '',
		'url': '',
		'title': ''
		}]
	twitter = [{
		'text': '',
		'url': '',
		'title': ''
		}]
	engineGoogle = Google(license=None, throttle=0.5, language=None)
	# engineBing = Bing(license=None, throttle=0.5, language=None)
	engineTwitter = Twitter(license=None, throttle=0.5, language=None)
	# engineFacebook = Facebook(license=None, throttle=1.0, language='en')
	# engineWikipedia = Wikipedia(license=None, throttle=5.0, language=None)
	# engineFlickr = Flickr(license=None, throttle=5.0, language=None)
	# engineArray = [engineGoogle, engineBing, engineTwitter, engineFacebook, engineWikipedia, engineFlickr]
	engineArray = [engineGoogle, engineTwitter]

	# Google
	for i in range(1, 2):
		for para in engineGoogle.search(search_query, type=SEARCH, start=i, count=5):
			google.append({ 'text': para.text, 'url': para.url, 'title': para.title })
		#resultGoogle = resultGoogle + ([para.text for para in engineGoogle.search(search_query, type=SEARCH, start=i, count=10)])
	# Twitter
	for i in range(1, 2):
		for para in engineTwitter.search(search_query, type=SEARCH, start=i, count=5):
			twitter.append({ 'text': para.text, 'url': para.url, 'title': para.title })
		#resultTwitter = resultTwitter + ([para.text for para in engineTwitter.search(search_query, type=SEARCH, start=i, count=10)])

	return { "Error": None, "Google": google, "Twitter": twitter}