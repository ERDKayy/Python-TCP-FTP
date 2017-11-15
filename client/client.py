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
        if s.recv(1024).decode('utf-8') == "OK":
            s.send(ready)
            bytes_remaining = s.recv(1024)
            bytes_remaining = int.from_bytes(bytes_remaining, byteorder='big', signed=False)
            original_size = bytes_remaining
            s.send(ok)
            toRecv = s.recv(min(bytes_remaining, 1024))

            # writes blocks to file while the data received is less than filesize
            while toRecv:
                print("%d of %d remaining..." % (bytes_remaining, original_size))
                f.write(toRecv)
                bytes_remaining = bytes_remaining - len(toRecv)
                toRecv = s.recv(min(bytes_remaining, 1024))

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
print(s.recv(1024), end='')
s.close()