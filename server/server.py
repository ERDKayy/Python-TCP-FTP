import sys
import socket               # Import socket module
import os


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(0)                 # Now wait for client connection.

while True:
    c, addr = s.accept()     # Establish connection with client.
    commandFile = c.recv(1024)
    commandFile = commandFile.decode("utf-8")
    commandFile = commandFile.split()
    file = commandFile[1]
    if commandFile[0] == "GET":
        file = commandFile[1]
        file = open(file, 'rb')
        toSend = file.read(1024)
        while toSend:
            print("sending...")
            c.sendall(toSend)
            toSend = file.read(1024)
        file.close()
        print("Done")

    if commandFile[0] == "PUT":
        file = open(file, 'wb')
        toRecv = c.recv(1024)
        while toRecv:
            print("receiving...")
            file.write(toRecv)
            toRecv = c.recv(1024)
        file.close()
        print("Done")

    if commandFile[0] == "DEL":
        os.remove(file)
        print("Done...")

    c.close()                # Close the connection
