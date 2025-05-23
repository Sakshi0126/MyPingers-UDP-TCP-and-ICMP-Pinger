import socket  
import time    
import sys     
import struct


 # Get the server IP , port no, no of pings
server_ip = '192.168.137.194'
server_port = 12005
num_of_pings = int(input("Enter number of pings: "))

# Initialize RTT statistics and packet loss counters
min_rtt = float('inf') 
max_rtt = 0             
total_rtt = 0           
lost_packets = 0        

icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

for seq_number in range(num_of_pings):
    # Create a new socket object for each ping
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Set a timeout of 2 seconds for the socket 
        sock.settimeout(2) 
        try:
            # Record the start time of the ping
            start_time = time.time()  
            # Connect to the server
            sock.connect((server_ip, server_port)) 
            # Create the ping message
            message = f"Ping {seq_number}".encode()
            # Send the ping message
            sock.sendall(message)  
            # Receive the server's response
            response = sock.recv(1024).decode()  
            # Record the end time of the ping
            end_time = time.time()  
            rtt = (end_time - start_time) * 1000  
            print(f"Received response from server: {response}")  
            print(f"RTT for packet {seq_number}: {rtt:.2f} ms") 

            # Update RTT statistics
            min_rtt = min(min_rtt, rtt) 
            max_rtt = max(max_rtt, rtt) 
            total_rtt += rtt           

        except socket.timeout:
            # Handle the case where the request times out
            print(f"Request timed out for the packet {seq_number}") 
            lost_packets = lost_packets + 1 

             # Try to receive ICMP packet
            icmp_packet, icmp_addr = icmp_sock.recvfrom(1024)

            recHeader = icmp_packet[20:28]
            recHeader = struct.unpack("bbHHh",recHeader)
            # icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq = struct.unpack('bbHHh', icmp_packet[:8])



            if recHeader[0] == 3:  # Destination unreachable
                print(f"ICMP error received: Destination unreachable (code {recHeader[1]})")
            elif recHeader[0] == 11:  # Time exceeded
                print(f"ICMP error received: Time exceeded (code {recHeader[1]})")
            else:
                print(f"ICMP error received: Type {recHeader[0]}, code {recHeader[1]}")



# Calculate packet loss rate and average RTT
packet_loss_rate = (lost_packets / num_of_pings) * 100 
if (num_of_pings - lost_packets) > 0:
    avg_rtt = total_rtt / (num_of_pings - lost_packets)  
else:
    avg_rtt = 0  # Avoid division by zero if all packets are lost

# Print the RTT statistics
print(f"\nMinimum RTT: {min_rtt:.2f} ms")
print(f"Maximum RTT: {max_rtt:.2f} ms")
print(f"Average RTT: {avg_rtt:.2f} ms") 
print(f"Packet loss rate: {packet_loss_rate:.2f}%") 

    
