# client 1
import socket
import threading

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.11"
port = 9999
msg_size = 1024
msg_format = 'utf-8'

# connect to server
client.connect((host, port))

def receive_msg():
    while True:
        try:
            msg_received = client.recv(msg_size).decode()
            if not msg_received:
                continue
            print(msg_received)
        except ConnectionAbortedError:
            print("Connection to server was aborted.")
            break

thread_receive = threading.Thread(target=receive_msg)
thread_receive.start()

while True:
    # Send message to server
    msg = input('>> ')
    client.send(msg.encode(msg_format))
    
    # check if message contains bye or exit to close program
    if msg.lower() == 'bye' or msg.lower() == 'exit':
        client.close()
        break


# close program
client.close()
