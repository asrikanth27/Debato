# Echo client program
import socket

host = '127.0.0.1'    # The remote host
port = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while port<50015:
    try:
        s.connect((host, port))
        break
    except (socket.error):
        print socket.error, ' ,port: ', port
        port += 1

while 1:
    query = raw_input('Enter data: ( 1 for exit ) :')
    if not query=='1':
        s.send(query)
    else:
        s.close()
        print 'Connection closed'
        exit(0)
s.send('Hello, world')
s.send('Bye Bye world')
try:
    while 1:
        data = s.recv(40)
        if data=='':
            s.close()
            raise KeyboardInterrupt
        print 'Received', repr(data), len(repr(data))
except KeyboardInterrupt:
    s.close()
    print 'Connection closed'
    exit(0)

# s.close()