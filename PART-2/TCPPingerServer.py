import socket  
import sys    


# Get the server IP address from command-line arguments
server_ip = '127.0.0.1'
# Get the server port number from command-line arguments and convert it to an integer
server_port = 12005

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    # Bind the socket to the address and port
    server_socket.bind((server_ip, server_port))
    # Enable the server to accept connections (0 means an unlimited number of connections in the queue)
    server_socket.listen(0)

    print(f"Server listening on {server_ip}:{server_port}")  # Print server startup message

    while True:
        # Accept an incoming connection
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")  # Print the address of the connected client
            while True:
                # Receive data from the client
                data = conn.recv(1024)
                # If no data is received, the client has closed the connection
                if not data:
                    break
                # Send the received data back to the client (echo)
                conn.sendall(data)

