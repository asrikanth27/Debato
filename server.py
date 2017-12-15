from flask import Flask, redirect, url_for, request
import main
app = Flask(__name__)

@app.route('/hello')
def hello_world():
   return 'Hello World'

@app.route('/debate', methods=["POST", "GET"])
def debate():
	main.run()
	return 'done'

# app.add_url_rule('/', 'hello', hello_world)

port = 5000
app.run('127.0.0.1', port, False)

if __name__ == '__main__':
   app.run()