#include <WiFi.h>
#include <WiFiUdp.h>

const char *WIFI_SSID = "SlimeServer";
const char *WIFI_PASS = "95815480";
const uint16_t UDP_PORT = 5000;

# define TX_BUF_LEN 1

WiFiUDP udp;
uint8_t rxBuffer[TX_BUF_LEN];
uint8_t txBuffer[TX_BUF_LEN];


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

  udp.beginPacket(udp.remoteIP(), udp.remotePort());
  udp.endPacket();

}