# Latency Test
Simple test for benchmarking UDP latency on an ESP32, specifically testing recieving packets at different intervals.

All results should be taken as rough estimates not absolute values.

# Testing

After some initial testing using `ping.py`, the most stable rtt results seemed to be from <10ms intervals while discarding the first result. Using these as a baseline, a value can be calculated that shows how "normal" a latency is. 

![Burst Analysis](/media/Default_settings.png)

In graphs this reffered to as `Send Delay`, Positive numbers represent higher latency in the PC -> ESP step compared to the baseline offset. Negative numbers represent better than baseline perfromance on that link side.

## Setup
All tests were run on an [ESP32C3-Supermini](https://www.aliexpress.us/item/3256801447048789.html), about 2 ft away from a dedicated router with only the testing PC via Ethernet and ESP32 via WiFi connected. 

During and in between tests nothing moved in the room, including electronics or people.

All tests were performed after ESP32 had atleast 5 minutes after connecting to wifi to come to operating temperature in free standing air.

## Results
The radio sleep time appears to have massive effects on latency, mostly resulting in negative effects beyond 50ms packet intervals. These negative effects can range anywhere from 800ms to 2400ms in some cases.



# Usage
> Platformio

Use ESP32C3 target or add your own (any esp32 model should work)

> Python

- `ping.py`: Sends a burst of packets at a fixed interval
- `run.py`: Gathers an average latency at range of intervals, dumps to `output.csv`
- `render.py`: Plots `output.csv` using matplotlib