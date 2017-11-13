import sys
import socket
import os

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Hostname to use
port = int(sys.argv[1])              # Port to be used

# connect to local machine with port given via args
s.connect((host, port))

# Take combined input and send to server via single packet
command = sys.argv[2]            # GET, PUT, or DEL
file = sys.argv[3]        # File path of file to transfer
toSend = str(command + " " + file).encode("utf-8")
s.send(toSend)

# if Get, open the file requested and write blocks as they are received
if command == "GET":
    f = open(file, 'wb')
    toRecv = s.recv(1024)
    fileSize = os.stat(file).st_size
    while toRecv:
        print("Receiving file %s (%d bytes)" % (file, fileSize))
        f.write(toRecv)
        toRecv = s.recv(1024)
        recvSize = os.stat(toRecv).st_size
        fileSize = (fileSize + recvSize)
    print("Done")

if command == "PUT":
    fileSize = os.stat(file).st_size
    f = open(file, 'rb')
    toSend = f.read(1024)
    while toSend:
        print("Sending file %s (%d bytes)" % (file, (fileSize / 1024)))
        s.sendall(toSend)
        toSend = f.read(1024)
        fileSize = (fileSize - 1024)
    f.close()
    print("Done")

s.shutdown(socket.SHUT_WR)
#print(s.recv(1024), end='')
s.close()