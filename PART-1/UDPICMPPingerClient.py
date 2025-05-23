import time
import socket
import sys
import struct

# Define server address and port
server_name = '192.168.172.122'  # for local testing
server_port = 12000

# Create a UDP socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Set a timeout of 1 second
client_sock.settimeout(1)

# Create a raw socket for ICMP
icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

# Getting no. of pings input from user
try:
    num_pings = int(input("Enter number of pings: "))
except ValueError:
    print("Invalid input! Please enter an integer.")
    sys.exit(1)

# Initialize variables
seq_number = 1
rtts_list = []
packet_loss = 0

# Sending N pings
while seq_number <= num_pings:
    # Create a message to send to the server
    send_time = time.time()
    message = "Ping {} {}".format(seq_number,send_time)

    try:
        # Send the message to the server
        client_sock.sendto(message.encode(), (server_name, server_port))
        start_time = time.time()

        # Wait for the response from the server
        data, server = client_sock.recvfrom(1024)
        end_time = time.time()

        # Calculating round-trip time (RTT)
        rtt = (end_time - start_time) * 1000  # Convert to milliseconds
        rtts_list.append(rtt)

        # Print response and RTT
        print(f"Received from server: {data.decode()}")
        print(f"RTT for packet #{seq_number}: {rtt:.2f} ms")
    except socket.timeout:
        # If no response from the server within timeout
        print(f"Request timed out for packet #{seq_number}")
        packet_loss += 1

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

    # Move to the next sequence number
    seq_number += 1

# Calculate and print minimum, maximum, and average RTT
if rtts_list:
    min_rtt = min(rtts_list)
    max_rtt = max(rtts_list)
    avg_rtt = sum(rtts_list) / len(rtts_list)
    print(f"\nMinimum RTT: {min_rtt:.2f} ms")
    print(f"Maximum RTT: {max_rtt:.2f} ms")
    print(f"Average RTT: {avg_rtt:.2f} ms")
else:
    print("\nNo successful pings.")

# Calculate and print packet loss rate
loss_rate = (packet_loss / num_pings) * 100
print(f"Packet Loss Rate: {loss_rate:.2f}%")

# Closing the sockets
client_sock.close()
icmp_sock.close()