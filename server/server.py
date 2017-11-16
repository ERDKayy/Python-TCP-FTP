import sys
import socket               # Import socket module
import os


verbose = False
try:
    if sys.argv[2] == "-v":
        verbose = True
except IndexError:
    pass


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])     # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(0)                 # Now wait for client connection.
if verbose == True:
    print("Server waiting on port %d" % (port))
errorCode = False

# Protocol messages
ready = "READY".encode("utf-8")
ok = "OK".encode("utf-8")
done = "DONE".encode("utf-8")





while True:
    c, addr = s.accept()     # Establish connection with client.
    address = str(addr)
    if verbose == True:
        print("Server connected to client at %s" % (address))
    c.send(ready)
    commandFile = c.recv(1024)
    commandFile = commandFile.decode("utf-8")
    if verbose == True:
        print("Server receiving request: %s" % (commandFile))
    commandFile = commandFile.split()
    file = commandFile[1]



    if commandFile[0] == "GET":

        try:
            f = open(file, 'rb')
        except IOError:
            error = "ERROR: " + file + " does not exist"
            c.send(error.encode('utf-8'))
            errorCode = True

        if errorCode == False:
            c.send(ok)
            readyCheck = c.recv(1024)
            if readyCheck.decode("utf-8") == "READY":
                fileSize = int(os.stat(file).st_size)
                c.send(fileSize.to_bytes(8, byteorder="big", signed=False))
                okCheck = c.recv(1024)
                if okCheck.decode("utf-8") == "OK":
                    if verbose == True:
                        print("Server sending %d bytes" % (fileSize))
                    toSend = f.read(1024)
                    while toSend:
                        c.sendall(toSend)
                        toSend = f.read(1024)
                    f.close()
                    c.send(done)

    if commandFile[0] == "PUT":
        c.send(ok)
        bytes_remaining = c.recv(1024)
        bytes_remaining = int.from_bytes(bytes_remaining, byteorder='big', signed=False)
        original_size = bytes_remaining
        c.send(ok)
        f = open(file, 'wb')
        toRecv = c.recv(min(bytes_remaining, 1024))
        if verbose == True:
            print("Server receiving %d bytes" % (original_size))
        while toRecv:
            #print("%d of %d remaining..." % (bytes_remaining, original_size))
            f.write(toRecv)
            bytes_remaining = bytes_remaining - len(toRecv)
            toRecv = c.recv(min(bytes_remaining, 1024))
        f.close()
        c.send(done)


    if commandFile[0] == "DEL":
        if verbose == True:
            print("Server deleting file %s" % (file))

        try:
            os.remove(file)
        except IOError:
            error = ("ERROR: %s does not exist" % (file))
            c.send(error.encode('utf-8'))

        c.send(done)

    c.close()                # Close the connection
