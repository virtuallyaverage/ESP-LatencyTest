import matplotlib.pyplot as plt
import csv

gaps = []
avg_first_rtts = []

with open('output.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gaps.append(float(row['gap_ms']))
        avg_first_rtts.append(float(row['avg_rtt_ms']))

plt.plot(gaps, avg_first_rtts, marker='o')
plt.xlabel("Time between packets (ms)")
plt.ylabel("Avg RTT (ms)")
plt.title("RTT vs Interval")
plt.show()