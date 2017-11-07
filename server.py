import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port


s.listen(0)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    received = c.recv(1024)
    received = received.decode("utf-8")
    if "GET" in received.upper():
        received = received.split()
        file = received[1]
        file = open(file, 'rb')
        toSend = file.read(1024)
        while file:
            print("sending...")
            c.sendall(toSend)
            toSend = file.read(1024)
        file.close()
    print("Done Receiving")
    c.close()                # Close the connection