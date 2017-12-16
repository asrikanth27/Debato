from flask import Flask, redirect, url_for, request, render_template, send_file
import main, os
import socket, queryServer, urllib2
app = Flask(__name__)


@app.route('/home')
def home():
   return render_template('customer.html')
   # return send_from_directory('')
   # print os.path.dirname(os.path.realpath(__file__)) + '/templates/customer.html'
   # return send_file(os.path.dirname(os.path.realpath(__file__)) + '/templates/customer.html')

@app.route('/debate', methods=["POST", "GET"])
def debate():
	# queryServer.fetchDataFromServer('Automation is bad for the economy.')
	if request.method == "GET":
		query =  urllib2.unquote(request.args.get('query')).decode('utf8')
		print 'GET method called haha!! ', query
	result = main.run(query, False)
	response_query = ''
	index = 1
	for para in result:
		response_query += str(index) + ') ' + para.encode('utf-8') + '\n'
		print str(index) + ') ' + para.encode('utf-8')
	return response_query


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