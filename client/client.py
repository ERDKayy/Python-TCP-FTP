import sys
import socket
import os

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Hostname to use
#port = int(sys.argv[1])     # Port to be used
port = 12345
# Client protocol messages
ready = "READY".encode("utf-8")
ok = "OK".encode("utf-8")


# connect to local machine with port given via args
s.connect((host, port))

# Take combined input and send to server via single packet
command = sys.argv[2]            # GET, PUT, or DEL
#command = "GET"
file = sys.argv[3]        # File path of file to transfer
#file = "asdaffsa.png"
toSend = str(command + " " + file).encode("utf-8")
#toSend = "GET asdaffsa.png".encode("utf-8")
readyCheck = s.recv(1024)

if readyCheck.decode("utf-8") == "READY":
    s.send(toSend)

    # if Get, open the file requested and write blocks as they are received
    if command == "GET":
        f = open(file, 'wb')
        okCheck = s.recv(1024).decode('utf-8')
        if okCheck == "OK":
            s.send(ready)
            bytes_remaining = s.recv(1024)
            bytes_remaining = int.from_bytes(bytes_remaining, byteorder='big', signed=False)
            original_size = bytes_remaining
            s.send(ok)
            toRecv = s.recv(min(bytes_remaining, 1024))

            # writes blocks to file while the data received is less than filesize
            print("Client receiving file %s (%d bytes)" % (file, original_size))
            while toRecv:
                #print("%d of %d remaining..." % (bytes_remaining, original_size))
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
        okCheck = s.recv(1024)

        if okCheck.decode('utf-8') == "OK":
            fileSize = os.stat(file).st_size
            s.send(fileSize.to_bytes(8, byteorder="big", signed=False))
            okCheck = s.recv(1024)

            if okCheck.decode('utf-8') == "OK":
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

    if command == "DEL":
        print("Client deleting file %s" % (file))
        doneCheck = s.recv(1024)
        if doneCheck.decode('utf-8') == "DONE":
            print("Complete")
        elif "ERROR" in doneCheck.decode('utf-8'):
            print("FUCKOFF")
s.shutdown(socket.SHUT_WR)
s.close()                # Close the connection
