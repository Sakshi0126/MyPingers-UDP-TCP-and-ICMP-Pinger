
import socket  
import threading  
import random 

server_ip = '127.0.0.1'
server_port = 12009

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to the specified IP address and port
server_socket.bind((server_ip, server_port))  

# Enable the socket to accept incoming connections
server_socket.listen()  

# Print a message indicating the server is listening
print(f"Server listening on {server_ip}:{server_port}") 




# Define a thread target function inline for handling client communication
def handle_client(connection, addr):
    with connection:
        print(f"Connected by {addr}")
        while True:
            data = connection.recv(1024) 
            if not data:
                break 
            
            # Simulate packet loss with a probability of 30%
            if random.random() < 0.3: 
                
                continue
            else:
                connection.sendall(data)  

    # Create and start a new thread to handle the client connection
while True:
    connection , addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, addr))
    client_thread.start()  

