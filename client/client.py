import sys
import socket
import os

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Hostname to use
port = int(sys.argv[1])     # Port to be used
#port = 12345

# Client protocol messages
ready = "READY".encode("utf-8")
ok = "OK".encode("utf-8")

command = "PUT"
file = "aaaaaaaaaaaa"

s.connect((host, port))
command = sys.argv[2]            # GET, PUT, or DEL
file = sys.argv[3]        # File path of file to transfer
#toSend = str(command + " " + file).encode("utf-8")
readyCheck = s.recv(1024)

if readyCheck.decode("utf-8") == "READY":
    #s.send(toSend)

    # if Get, open the file requested and write blocks as they are received
    if command == "GET":
        toSend = str(command + " " + file).encode("utf-8")
        s.send(toSend)
        okCheck = s.recv(1024).decode('utf-8')

        if okCheck == "OK":
            try:
                f = open(file, 'wb')
            except IOError:
                print("Client error: unable to create file " + file)
                s.close()
                sys.exit()
            s.send(ready)
            bytes_remaining = s.recv(1024)
            bytes_remaining = int.from_bytes(bytes_remaining, byteorder='big', signed=False)
            original_size = bytes_remaining
            s.send(ok)
            toRecv = s.recv(min(bytes_remaining, 1024))

            # writes blocks to file while the data received is less than filesize
            print("Client receiving file %s (%d bytes)" % (file, original_size))
            while toRecv:
                f.write(toRecv)
                bytes_remaining = bytes_remaining - len(toRecv)
                toRecv = s.recv(min(bytes_remaining, 1024))
            doneCheck = s.recv(1024)
            if doneCheck.decode('utf-8') == "DONE":
                print("Complete")
        elif "ERROR" in okCheck:
            okCheck = okCheck.split("ERROR: ")
            print("Server error: file %s" % (okCheck[1]))

    # if PUT; open file, read bytes into packets and send
    if command == "PUT":
        try:
            f = open(file, 'rb')
        except IOError:
            print("Client error: " + file + " does not exist")
            s.close()
            sys.exit()
        toSend = str(command + " " + file).encode("utf-8")
        s.send(toSend)
        okCheck = s.recv(1024)

        if okCheck.decode('utf-8') == "OK":
            fileSize = os.stat(file).st_size
            s.send(fileSize.to_bytes(8, byteorder="big", signed=False))
            okCheck = s.recv(1024)
            okCheck = okCheck.decode('utf-8')

            if okCheck == "OK":
                f = open(file, 'rb')
                toSend = f.read(1024)
                print("Client sending file %s (%d bytes)" % (file, fileSize))

                while toSend:
                    s.sendall(toSend)
                    toSend = f.read(1024)
                f.close()
                doneCheck = s.recv(1024)

                if doneCheck.decode('utf-8') == "DONE":
                    print("Complete")
            elif "ERROR" in okCheck:
                okCheck = okCheck.split("ERROR: ")
                print("Server error: %s" % (okCheck))

    if command == "DEL":
        toSend = str(command + " " + file).encode("utf-8")
        s.send(toSend)
        print("Client deleting file %s" % (file))
        doneCheck = s.recv(1024)
        doneCheck = doneCheck.decode('utf-8')
        if doneCheck == "DONE":
            print("Complete")
        elif "ERROR" in doneCheck:
            doneCheck = doneCheck.split("ERROR: ")
            print("Server error: file %s" % (doneCheck[1]))


s.shutdown(socket.SHUT_WR)
s.close()                # Close the connection
