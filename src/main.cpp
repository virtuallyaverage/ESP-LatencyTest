#include <WiFi.h>
#include <WiFiUdp.h>

const char *WIFI_SSID = "SlimeServer";
const char *WIFI_PASS = "95815480";
const uint16_t UDP_PORT = 5000;

// packets used for clock offset syncing
// requests for the sync packet from the esp32
#define SYNC_REQ  0 
// esp32 sends T1 timestamp in microseconds as int64
#define SYNC      1
// local time 
#define SYNC_RESP 2

// Packets used for actual ping tests
#define PING 2
#define PONG 3


WiFiUDP udp;
uint8_t rxBuffer[8];
int64_t now;

void setup()
{
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  //WiFi.setSleep(WIFI_PS_NONE); //        COMMENT ME OUT

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
  // If we recieved a packet throw a return packet as quickly as possible
  int packetSize = udp.parsePacket();
  if (packetSize == 0)
    return;
  udp.read(rxBuffer, packetSize);
  now = esp_timer_get_time();

  udp.beginPacket(udp.remoteIP(), udp.remotePort());
  udp.write((uint8_t*)&now, sizeof(now));
  udp.endPacket();

}