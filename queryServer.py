import socket

def fetchDataFromServer(ip_addr, input_string):
    try:
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        print "Socket created successfully"
    except socket.error as err:
        print "Socket creation failed: ",err
    default_port = 8000
    s.connect((ip_addr, default_port))
    print "Socket successfully connected to the server on port:",default_port
    
    s.sendall(str(input_string))
    data =  s.recv(1024)
    s.close()

    print "Data Received"
    return str(data)