from flask import Flask, redirect, url_for, request, render_template, send_file
import main, os
import socket, urllib2, json
app = Flask(__name__)

# -------------------------------------------------------------------------------------

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

# -------------------------------------------------------------------------------------


@app.route('/home')
def home():
   return render_template('chat_new.html')
   # return send_from_directory('')
   # print os.path.dirname(os.path.realpath(__file__)) + '/templates/customer.html'
   # return send_file(os.path.dirname(os.path.realpath(__file__)) + '/templates/customer.html')

@app.route('/debate', methods=["POST", "GET"])
@crossdomain(origin='*')
def debate():
	# queryServer.fetchDataFromServer('Automation is bad for the economy.')
	if request.method == "GET":
		query =  urllib2.unquote(request.args.get('query')).decode('utf8')
		print 'GET method called haha!! ', query
	elif request.method == "POST":
		query = request.form['query']

	print '\nQuery: ', query
	results = main.run(query, True)
	# results = ['hello']
	response_query = ''
	index = 0
	def force_to_unicode(text):
		return text if isinstance(text, unicode) else text.decode('utf8')
	# try:		# TODO: check TypeError
	for para in results:
		try:
			response_query += str(index) + ') ' + para + '\n'# force_to_unicode(para) + '\n'
			# results[index] = para# force_to_unicode(para)
			print str(index) + ') ' + para# force_to_unicode(para)
		except (TypeError):
			print 'TypeError in para in results...'
		index += 1
	# except (TypeError):
		# print 'TypeError before para in results...'
	return json.dumps(results)


@app.route('/chat')
def chat():
	HOST = '127.0.0.1'    # The remote host
	PORT = 50007              # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.send('Hello, world')
	data = s.recv(1024)
	s.close()
	print 'Received', repr(data)

# app.add_url_rule('/', 'hello', hello_world)

port = 5000
app.run('127.0.0.1', port, False)

if __name__ == '__main__':
   app.run()