#server
import socket
import threading

# create socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define variables and their values
host = "192.168.1.11"   #ip address of server
port = 9999             #port number
msg_size = 1024         #message size
msg_format = 'utf-8'    #message format

# bind socket to the host and port
server.bind((host, port))

# listen for incoming connections
server.listen()

# store connections
clients = []

# function to handle messages received and sent
def msg_handling(client):
    while True:
        # receive messages from client
        msg = client.recv(msg_size).decode(msg_format)
        # check if client sent bye or exit to close and remove the client from server
        if msg.lower() == "bye" or msg.lower() == "exit":
            if client in clients:
                clients.remove(client)
            break
        # send message to all connected clients
        broadcast(msg, sender=client)

# function to send messages to connected clients
def broadcast(msg, sender=None):
    # send message to each client
    for client in clients:
        if client != sender:
                client.send(msg.encode(msg_format))

# function to accept incoming connections and add them to the clients list
def accept_client(): 
    print("Waiting for connections...")
    while True:
        # accept incoming conenction
        client, address = server.accept()
        print(f"Got a connection from {address}")
        # add to client list
        clients.append(client)
        
        # start thread for message handling
        msg_thread = threading.Thread(target=msg_handling, args=(client,))
        msg_thread.start()

# start thread for accepting connection        
thread = threading.Thread(target=accept_client)
thread.start()
