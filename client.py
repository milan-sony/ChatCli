import socket
import threading

host = '127.0.0.1'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"Connecting to {host}:{port}...")

# connect to the server
server_socket.connect((host, port))
print("Connected to server")

name = input("Enter your name: ")

def listen_for_messages():
    while True:
        message = server_socket.recv(1024).decode('utf-8')
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = threading.Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
print("Thread started")

while True:
    # message to send to the server
    message_to_send = input()
    if message_to_send.lower() == 'exit':
        break
    server_socket(message_to_send.encode('utf-8'))

server_socket.close()
