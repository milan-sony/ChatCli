# chat_server.py

import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'exit':
                print("Client has disconnected.")
                break
            print(f"Client: {message}")
            response = input("You: ")
            client_socket.send(response.encode('utf-8'))
        except:
            print("An error occurred.")
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))  # Bind to all interfaces on port 12345
    server.listen(5)  # Allow 5 pending connections
    print("Server listening on port 12345...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
