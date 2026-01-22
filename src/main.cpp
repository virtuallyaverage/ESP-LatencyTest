#include <WiFi.h>
#include <WiFiUdp.h>
#include "esp_wifi.h"

//  50_000 peak @ ~95 interval with ~4ms (forgot to save csv, pretty much noise)
//  75_000 peak @ ~55 interval with ~22ms (peaks at 55, 130, 203; intervals of ~75)
// 100_000 peak @ ~60 interval with ~42ms
// 150_000 peak @ ~62 interval with ~86ms
// 200_000 peak @ ~58 interval with ~130ms
// linear regression on wake intervals shows values sub ~45ms are indistinguishable from noise
// x; wake packet interval
// y; round trip latency
// a=0.847586
// b=-40.67241 
// R^2 = 0.9989 

#define RETURN_PACKET_INTERVAL_US 100000 /*microseconds*/

const char *WIFI_SSID = "SlimeServer";
const char *WIFI_PASS = "95815480";
const uint16_t UDP_PORT = 5000;

bool first = false;
WiFiUDP udp;
uint8_t rxBuffer[8];
int64_t now;
int64_t next;
uint8_t zero = 0;

void setup()
{
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected. IP: ");
  Serial.println(WiFi.localIP());

  udp.begin(UDP_PORT);
  Serial.printf("UDP server listening on port %d\n", UDP_PORT);
}

void loop()
{

  int packetSize = udp.parsePacket();
  // If we recieved a packet throw a return packet as quickly as possible
  if (packetSize != 0)
  {
    if (!first)
    {           // is absorbed into the first warmup sequence and discarded.
      delay(5); // Allow ARP to resolve on first packet (I think?)
      first = true;
    }

    udp.read(rxBuffer, packetSize);
    now = esp_timer_get_time();
    next = now + RETURN_PACKET_INTERVAL_US;

    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    int wrote = udp.write((uint8_t *)&now, sizeof(now));
    udp.endPacket();
  }
  // wake our radio at interval.
  else if (first && esp_timer_get_time() > next)
  {
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.write(&zero, sizeof(uint8_t));
    udp.endPacket();
    next = esp_timer_get_time() + RETURN_PACKET_INTERVAL_US;
  }
}