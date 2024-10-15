import socket
import threading

# an empty list to store/remove other client sockets
client_sockets = []

def client_handle(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            message = cs.recv(1024).decode('utf-8')
        except Exception as e:
            print(f"Error handling client: {e}")
            # removes the client socket
            client_sockets.remove(cs)

        for client_socket in client_sockets:
            # iterate over all connected sockets and sends the message
            client_socket.send(message.encode('utf-8'))
            print("sent message")

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """
    created a socket object called server_socket. This socket acts as a communication endpoint for the server. The socket function from the socket module is used to create this socket object. We pass two arguments to this function:
    """

    """
    socket.AF_INET: This argument specifies the address family for the socket, which, in this case, is the Internet Protocol version 4 (IPv4) addressing. It stands for "Address Family - Internet.

    socket.SOCK_STREAM: This argument specifies the socket type, which is TCP (Transmission Control Protocol) in this case. TCP is a reliable, connection-oriented protocol used for data transmission. It stands for "Socket Type - Stream."
    """

    # bind() binds the socket to a specific IP and port so that it can listen to incoming requests on that IP and port

    try:
        server_socket.bind((host, port))

        # listen() method puts the server into listening mode
        server_socket.listen(5)

        print(f"Server listening on {host}:{port}")
        while True:
            # accept method initiates a connection with the client
            # we keep listening for new connections all the time
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            # adding the new connected client to client_sockets[]
            client_sockets.append(client_socket)
            print("client appended")
            # starts a new thread that listens for each client's messages
            t = threading.Thread(target = client_handle, args=(client_socket))
            # makes a thread daemon so it ends whenever the main thread ends
            t.daemon = True
            # starts the thread
            t.start()
            print("Thread started")
    except KeyboardInterrupt:
        print("Server is shutting down")
    except Exception as e:
        print(f'Error starting the server: {e}')
    finally:
        for cs in client_sockets:
            # closes all the client socket
            cs.close()
        # closes the server socket
        server_socket.close()
        print("Server socket closed")


if __name__ == "__main__":
    main()
