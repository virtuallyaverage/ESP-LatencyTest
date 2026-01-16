import matplotlib.pyplot as plt
import csv

gaps = []
avg_rtts = []
send_delays = []

with open('output.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gaps.append(float(row['gap_ms']))
        avg_rtts.append(float(row['avg_rtt_ms']))
        send_delays.append(float(row['avg_send_delay']))


plt.plot(gaps, avg_rtts, marker='o', markersize=3, label='RTT')
plt.plot(gaps, send_delays, marker='^', markersize=3, label='Relative Send Delay')
plt.xlabel("Time between packets (ms)")
plt.ylabel("Time (ms)")
plt.title("RTT vs Interval")
plt.legend()
plt.show()