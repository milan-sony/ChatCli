import socket
import threading

# Create a client socket to connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def listen_for_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Disconnected from server")
                break
            print("\n" + message)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def main():
    host = '127.0.0.1'
    port = 12345

    print(f"Connecting to {host}:{port}")

    # connect to the server
    client_socket.connect((host, port))
    print("Connected to server")

    # make a thread that listens for messages to this client & print them
    t = threading.Thread(target = listen_for_messages)
    t.daemon = True
    t.start()
    print("Thread started")

    username = input("Enter your name: ")

    while True:
        # message to send to the server
        message_to_send = input()
        full_message = f"{username}: {message_to_send}"
        if message_to_send.lower() == 'exit':
            print("Disconnected from server")
            client_socket.close()
            break
        client_socket.send(full_message.encode('utf-8'))

if __name__ == "__main__":
    main()
