import sys
import socket
import os

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Hostname to use
port = int(sys.argv[1])     # Port to be used

# Client protocol messages
ready = "READY".encode("utf-8")
ok = "OK".encode("utf-8")


# connect to local machine with port given via args
s.connect((host, port))

# Take combined input and send to server via single packet
command = sys.argv[2]            # GET, PUT, or DEL
file = sys.argv[3]        # File path of file to transfer
toSend = str(command + " " + file).encode("utf-8")
readyCheck = s.recv(1024)

if readyCheck.decode("utf-8") == "READY":
    s.send(toSend)
    # if Get, open the file requested and write blocks as they are received
    if command == "GET":
        f = open(file, 'wb')
        s.send(ready)
        fileSize = s.recv(1024)
        s.send(ok)
        toRecv = s.recv(1024)
        #fileSize = os.stat(file).st_size
        while toRecv:
            #print("Receiving file %s (%d bytes)" % (file, fileSize))
            if toRecv.decode("utf-8") == "DONE":
                sys.exit("Complete")
            f.write(toRecv)
            toRecv = s.recv(1024)
            #recvSize = os.stat(toRecv).st_size
            #bytesRemaining = fileSize - recvSize
            #print("Bytes Remaining: %d" % (bytesRemaining))
            #fileSize = (fileSize + recvSize)
        print("Done")
    # if PUT; open file, read bytes into packets and send
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