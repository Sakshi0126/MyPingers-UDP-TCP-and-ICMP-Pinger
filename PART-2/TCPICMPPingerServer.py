
import socket  
import threading  
import random 
import struct


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]

        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


server_ip = '127.0.0.1'
server_port = 12000

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified IP address and port
server_socket.bind((server_ip, server_port))  

# Enable the socket to accept incoming connections
server_socket.listen()  

#icmp socket
icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

# Print a message indicating the server is listening
print(f"Server listening on {server_ip}:{server_port}") 



while True:
    connection, addr = server_socket.accept() 
    
    print(f"Connected by {addr}") 

    # Define a thread target function inline for handling client communication
    def handle_client(conneection, addr):
        with connection:
            while True:
                data = connection.recv(1024) 
                if not data:
                    break 
                
                # Simulate packet loss with a probability of 30%
                if random.random() < 0.3: 
                    icmp_type = 3  # Destination unreachable
                    icmp_code = 0  # Network unreachable
                    icmp_checksum = 0
                    icmp_id = 0
                    icmp_seq = 0

                    icmp_packet = struct.pack('bbHHh', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
                    icmp_checksum = checksum(icmp_packet)
                    icmp_packet = struct.pack('bbHHh', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

                    icmpSocket.sendto(icmp_packet, addr)
                    continue
                    
                else:
                    connection.sendall(data)  

    # Create and start a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(connection, addr))
    client_thread.start()  
