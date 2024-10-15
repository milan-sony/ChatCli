import socket
import threading

# An empty list to store/remove other client sockets
client_sockets = []
client_sockets_lock = threading.Lock()  # To handle thread safety

def client_handle(cs):
    """
    This function keeps listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients.
    """
    while True:
        try:
            message = cs.recv(1024).decode('utf-8')
            if not message:
                break  # No message means the client disconnected
            # Broadcast the message to all other clients
            with client_sockets_lock:  # Lock the client_sockets list
                for client_socket in client_sockets:
                    if client_socket != cs:  # Avoid sending the message back to the sender
                        client_socket.send(message.encode('utf-8'))
            print("sent message")
        except Exception as e:
            print(f"Error handling client: {e}")
            break  # Exit the loop on error

    # Remove the client socket upon disconnection
    with client_sockets_lock:
        client_sockets.remove(cs)
        cs.close()

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            with client_sockets_lock:
                client_sockets.append(client_socket)
                print("client appended")

            t = threading.Thread(target=client_handle, args=(client_socket,))
            t.daemon = True
            t.start()
            print("Thread started")
    except KeyboardInterrupt:
        print("Server is shutting down")
    except Exception as e:
        print(f'Error starting the server: {e}')
    finally:
        # Clean up all client sockets and server socket
        with client_sockets_lock:
            for cs in client_sockets:
                cs.close()
        server_socket.close()
        print("Server socket closed")

if __name__ == "__main__":
    main()
