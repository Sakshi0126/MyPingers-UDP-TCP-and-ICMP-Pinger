import socket  
import time    
import sys     



 # Get the server IP , port no, no of pings
server_ip = '127.0.0.1'
server_port = 12009
num_of_pings = int(input("Enter number of pings: "))

# Initialize RTT statistics and packet loss counters
min_rtt = float('inf') 
max_rtt = 0             
total_rtt = 0           
lost_packets = 0        

 # Create a new socket object for each ping
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 # Connect to the server
sock.connect((server_ip, server_port)) 

for seq_number in range(num_of_pings):
   
    
        # Set a timeout of 2 seconds for the socket 
        sock.settimeout(2) 
        try:
            # Record the start time of the ping
            start_time = time.time()  
           
            
            # Create the ping message
            
            message = ("Ping {} {}".format(seq_number,start_time)).encode() 
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

    
