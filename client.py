import sys
import socket
s = socket.socket()         # Create a socket object
host = sys.argv[1]
port = int(sys.argv[2])     # Port to be used
command = sys.argv[3]
file = sys.argv[4]


# connect to local machine with port given via args
s.connect((socket.gethostname(), port))
f = open(file,'rb')
print('Sending...')
l = f.read(1024)
while (l):
    print('Sending...')
    s.sendall(l)
    l = f.read(1024)
f.close()
print("Done Sending")
s.shutdown(socket.SHUT_WR)
print(s.recv(1024))
s.close()