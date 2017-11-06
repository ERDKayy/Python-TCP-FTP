import sys
import socket
s = socket.socket()         # Create a socket object
host = sys.argv[1]          # Hostname to use
port = int(sys.argv[2])     # Port to be used
command = sys.argv[3]       # GET, PUT, or DEL
file = sys.argv[4]          # File path of file to transfer


# connect to local machine with port given via args
s.connect((host, port))
f = open(file,'rb')

if command.upper() == 'PUT':
    print('Sending...')
    l = f.read(1024)
    while l:
        print('Sending...')
        s.sendall(l)
        l = f.read(1024)
    f.close()
print("Done")
s.shutdown(socket.SHUT_WR)
print(s.recv(1024))
s.close()