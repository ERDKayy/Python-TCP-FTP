import sys
import socket               # Import socket module
import os


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(0)                 # Now wait for client connection.

# Protocol messages
ready = "READY".encode("utf-8")
ok = "OK".encode("utf-8")
done = "DONE".encode("utf-8")

while True:
    c, addr = s.accept()     # Establish connection with client.
    c.send(ready)
    commandFile = c.recv(1024)
    commandFile = commandFile.decode("utf-8")
    commandFile = commandFile.split()
    file = commandFile[1]


    if commandFile[0] == "GET":
        c.send(ok)
        readyCheck = c.recv(1024)
        if readyCheck.decode("utf-8") == "READY":
            file = commandFile[1]
            f = open(file, 'rb')
            fileSize = os.stat(file).st_size
           	c.send(fileSize.toBytes(8, byteorder = "big", signed = false)
            okCheck = c.recv(1024)
            if okCheck.decode("utf-8") == "OK":
                toSend = f.read(1024)
                while toSend:
                    print("sending...")
                    c.sendall(toSend)
                    toSend = f.read(1024)
                file.close()
                c.send(done)

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
