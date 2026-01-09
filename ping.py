import socket
import time
import matplotlib.pyplot as plt

UDP_IP = "192.168.1.105"
UDP_PORT = 5000
NUM_PINGS = 200

BURST_SIZE = 100
PING_DELAY = 0.010

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(3.0)

times = []
timestamps = []
start_time = time.perf_counter()
for i in range(BURST_SIZE):
    start = time.perf_counter()
    sock.sendto(b'\x00', (UDP_IP, UDP_PORT))
    try:
        sock.recvfrom(1024)
        rtt = (time.perf_counter() - start) * 1000
        times.append(rtt)
        timestamps.append(start - start_time)
    except socket.timeout:
        print(f"Burst ping {i+1}: timeout")
    
    time.sleep(PING_DELAY)
    

sock.close()

plt.scatter(timestamps, times)
plt.ylim(-4, 500)
plt.xlabel("Time (s)")
plt.ylabel("RTT (ms)")
plt.title(f"UDP RTT (avg: {sum(times)/len(times):.2f} ms)")
plt.show()