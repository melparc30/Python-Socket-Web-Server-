import socket

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
# host = socket.gethostname()
host = "localhost"
port = 8080

# bind to the port
server.bind((host, port))

# listen for the incoming connection
server.listen()
print("Waiting for connections...")

while True:
    # accept connections
    client, address = server.accept()
    print(f"Got a connection from {address}")
    
    #get client request
    request = client.recv(1024)
    if not request:
        break
    request = request.decode()
    print(request)
    
    # extract requested file type
    requested_file = request.split()[1].lstrip('/')
    
    #check if file has image
    if requested_file.endswith(".png"):
        #get content of image file
        file = open(requested_file, "rb")
        content = file.read()
        file.close()
        #send response
        response = b'HTTP/1.0 200 OK\nContent-Type: image/png\n\n' + content
    #check if file has css
    elif requested_file.endswith(".css"):
        # get content of css file
        file = open(requested_file, "r")
        content = file.read()
        file.close()
        # send response
        response = b'HTTP/1.0 200 OK\nContent-Type: text/css\n\n' + content.encode()
    else:
        #get content of html file
        file = open("index.html", "r")
        content = file.read()
        file.close()
        #send response
        response = b'HTTP/1.0 200 OK\nContent-Type: text/html\n\n' + content.encode()
    
    #send response
    client.sendall(response)
    #close connection
    client.close()

#close server
server.close()