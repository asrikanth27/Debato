# Echo server program
import socket, main

host = ''                 # Symbolic name meaning the local host
port = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while port<50015:
	try:
		s.bind((host, port))
		break
	except socket.error, v:
		if v[0] == 98:
			print 'Socket error, port: ', port, ', v: ', v[0], ' already in use!!'
			port += 1
		else:
			exit(0)

# s.bind((host, port))
s.listen(5)
conn, addr = s.accept()
print 'Connected by', addr

def new_conn():
	conn, addr = s.accept()
	print 'New connection'

try:
	while 1:
	    data = conn.recv(1024)
	    string = bytes.decode(data)
	    print 'Data: ', data
	    # print 'Lol!!'
	    if data=='':
	    	conn.close()
	    	print 'Waiting for new connection...'
	    	conn, addr = s.accept()
	    	# new_conn()
	    	# raise KeyboardInterrupt
	    else:
	    	print 'Recieved from node...'
	    	main.run(str(data))
	    	conn.send('Message recieved')
	conn.close()
except (KeyboardInterrupt, socket.error):
	conn.close()
	s.close()
	print 'Connection closed'
	exit(0)