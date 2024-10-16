# chat_client.py

import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
# print(IPAddr)

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = IPAddr # E.g., '192.168.1.5'
    client.connect((server_ip, 12345))  # Connect to the server on port 12345

    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            client.send(message.encode('utf-8'))
            break
        client.send(message.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(f"Server: {response}")

    client.close()

if __name__ == "__main__":
    start_client()
