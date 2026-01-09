import socket
import time
import matplotlib.pyplot as plt

UDP_IP = "192.168.1.105"
UDP_PORT = 5000

START_GAP = 0.001
STEP_GAP = 0.004
NUM_GAPS = 500000
REPETITIONS = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(3.0)

gaps = []
avg_first_rtts = []

try:
    for g in range(NUM_GAPS):
        gap = START_GAP + g * STEP_GAP
        first_rtts = []
        
        for rep in range(REPETITIONS + 1):
            time.sleep(gap)

            start = time.perf_counter()
            sock.sendto(b'\x00', (UDP_IP, UDP_PORT))
            try:
                sock.recvfrom(255)
                rtt = (time.perf_counter() - start) * 1000
                if rep != 0: # ignore first value
                    first_rtts.append(rtt)
            except socket.timeout:
                print(f"Gap {gap*1000:.0f}ms, rep {rep+1}, ping: timeout")
        
        gaps.append(gap * 1000)
        avg_first_rtts.append(sum(first_rtts) / len(first_rtts) if first_rtts else 0)
        print(f"{gap*1000:.0f},{avg_first_rtts[-1]:.2f}")

except KeyboardInterrupt:
    print("\nPlotting data")

sock.close()

plt.plot(gaps, avg_first_rtts, marker = 'o')
plt.xlabel("Time between packets (ms)")
plt.ylabel("Avg RTT (ms)")
plt.title("RTT vs Interval")
plt.show()