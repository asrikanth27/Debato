from flask import Flask, redirect, url_for, request
import main
import socket
app = Flask(__name__)

def getResponse(input_string):
    return main.run(input_string)

@app.route('/hello')
def hello_world():
   return 'Hello World'

@app.route('/debate', methods=["POST", "GET"])
def debate(input_string):
	main.run(input_string)
	return 'done'


@app.route('/testsocket')
def test_socket():
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 8000              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)
        if not data: break
        response = getResponse(str(data))
        conn.sendall(response)
    conn.close()

# app.add_url_rule('/', 'hello', hello_world)

port = 5000
app.run('127.0.0.1', port, False)

if __name__ == '__main__':
   app.run()