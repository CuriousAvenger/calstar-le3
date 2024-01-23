#include <WiFi.h>

const char* ssid = "Nice";
const char* passwd = "piii4305";

const char* ip_addr = "192.168.174.91";
const int port_send = 4444;
const int port_recv = 4445;

void connect_to_wifi(const char* ssid, const char* password) {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("[SYSTEM] Waiting for Wifi to appear");
    delay(1000);
  }
  Serial.print("[SYSTEM] Connected to WIFI with IP:");
  Serial.println(WiFi.localIP());
}

void send(void *parameter) {
  WiFiClient client_send;
  while (true) {
    while (!client_send.connect(ip_addr, port_send)) {
      Serial.println("[SEND] Waiting for COM Server to appear ");
      delay(1000);
    }
    Serial.println("[SEND] DAQ-COM Connection Established");

    while (true) {
      if (client_send.connected()) {
        char buffer[32];
        dtostrf(100, 5, 3, buffer);
        client_send.write(buffer);
      } else {
        Serial.println("[SEND] COM Connection Reset");
        break;
      }
      delay(50);
    }
  } 
}

void recv(void* parameter) {
  WiFiServer server(port_recv);
  server.begin();
  Serial.print("[RECV] Receving Server Started: ");
  Serial.println(WiFi.localIP());
  WiFiClient client_recv = server.available();

  while (true) {
    while (!client_recv) {
      Serial.println("[RECV] Waiting for COM Server to appear");
      client_recv = server.available();
      delay(2000);
    }
    Serial.println("[RECV] DAQ-COM Connection Established");
    
    if (client_recv) {
      while (client_recv.connected()) {
        String data = client_recv.readStringUntil('\n');
        if (!data.isEmpty()) {
          Serial.println("[RECV] Received: " + data);
        }
      }
    } else {
      Serial.println("[RECV] COM Connection Reset");
      client_recv.stop();
    }
  }
}

TaskHandle_t sendThread, recvThread;
void setup() {
  Serial.begin(115200);
  connect_to_wifi(ssid, passwd);

  xTaskCreatePinnedToCore(
    send, "sendThread", 10000, NULL, 1, &sendThread, 0);
  xTaskCreatePinnedToCore(
    recv, "recvThread", 10000, NULL, 1, &recvThread, 1);
}

void loop() {}