import socket
import time
import struct

UDP_IP = "192.168.1.101"
UDP_PORT = 5000

START_GAP = 0.005
STEP_GAP = 0.005
NUM_GAPS = 60
REPETITIONS = 10

WARMUP_OFFSET = 50

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(3.0)

# Get's rough clock offset, in microseconds, this offset includes the 2-3 ms wifi transmit delay.
def getClockOffset(sock: socket.socket, rep = WARMUP_OFFSET) -> int:
    offset = 0
    for i in range(rep+1):
        send_time_us = int(time.perf_counter() * 1_000_000)
        sock.sendto(struct.pack('<q', send_time_us), (UDP_IP, UDP_PORT))
        try:
            while True:
                data, _ = sock.recvfrom(255)
                if len(data) >= 8:  # Timestamp response
                    esp_time_us = struct.unpack('<q', data[:8])[0]
                    break
            if i != 0: # Skip first packet interruption
                offset += send_time_us - esp_time_us
        except socket.timeout:
            print(f"{rep+1}, clock offset: timeout")
            return int(offset / (i+1) )
    return int(offset / rep)


with open("output.csv", "w") as f:
    f.write("gap_ms,avg_rtt_ms,avg_send_delay,mcu_clk_offset\n")
    try:
        #
        for g in range(NUM_GAPS):
            offset = getClockOffset(sock)
            gap = START_GAP + g * STEP_GAP
            first_rtts = [] # entire ping pong duration
            send_delay = [] # delay between our sent packet and MCU recieving
            
            for rep in range(REPETITIONS + 1):
                time.sleep(gap)

                start = time.perf_counter()
                sock.sendto(struct.pack('<q', int(start * 1_000_000)), (UDP_IP, UDP_PORT))
                try:
                    esp_time_us = 0
                    while True:
                        data, _ = sock.recvfrom(255)
                        if len(data) > 1:  # Timestamp response
                            esp_time_us = struct.unpack('<q', data[:8])[0]
                            break
                    rtt = (time.perf_counter() - start) * 1000
                    if rep != 0:
                        send_delay.append(((esp_time_us + offset) / 1_000) - (start * 1_000))
                        first_rtts.append(rtt)
                except socket.timeout:
                    print(f"Gap {gap*1000:.0f}ms, rep {rep+1}, ping: timeout")
            
            gap_ms = gap * 1000
            avg_rtt = sum(first_rtts) / len(first_rtts) if first_rtts else 0
            avg_send_delay = sum(send_delay) / len(send_delay) if send_delay else 0
            f.write(f"{gap_ms:.0f},{avg_rtt:.2f},{avg_send_delay:.2f},{offset/1000}\n")
            print(f"gap:{gap_ms:.0f},rtt:{avg_rtt:.2f},avg_send_delay:{avg_send_delay:.2f},clk_offset:{offset/1000}")

    except KeyboardInterrupt:
        print("\nStopped early, data saved")

sock.close()