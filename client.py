import sys
import socket
s = socket.socket()         # Create a socket object
host = socket.gethostname()          # Hostname to use
port = 12345     # Port to be used
command = "GET"       # GET, PUT, or DEL
file = "tosend.png"      # File path of file to transfer


# connect to local machine with port given via args
s.connect((host, port))

if command == "GET":
    toSend = str(command + " " + file).encode("utf-8")
    s.send(toSend)
    f = open(file, 'wb')
    print("Receiving...")
    toRecv = s.recv(1024)
    while toRecv:
        print("Receiving...")
        f.write(toRecv)
        toRecv = s.recv(1024)
    toRecv.close()
    print("Done")

s.shutdown(socket.SHUT_WR)
print(s.recv(1024), end='')
s.close()