#include <WiFi.h>

const char* ssid = "RPI-DAQ";
const char* passwd = "password123";

const char* ip_addr = "192.168.4.1";
const int port_send = 4444;
const int port_recv = 4445;

void connect_to_wifi(const char* ssid, const char* password) {
  int i = 0;
  WiFi.begin(ssid, password);
  Serial.print("[SYSTEM] Waiting for Wifi to appear\n[");
  while (WiFi.status() != WL_CONNECTED) {
    i++;
    Serial.print(".");
    delay(100);
    if (i>10) {
      ESP.restart();
    }
  }
  Serial.print("\n[SYSTEM] Connected to WIFI with IP:");
  Serial.println(WiFi.localIP());
  // print some information regarding the wifi here
}

void send(void *parameter) {
  while (true) {
    WiFiClient client_send;

    while (!client_send.connect(ip_addr, port_send)) {
      Serial.println("[SEND] Waiting for DAQ-RPI Server to appear");
      delay(100);
    }
    Serial.println("[SEND] DAQ-RPI Connection Established");

    while (client_send.connected()) {
      char buffer[64];
      uint64_t time = esp_timer_get_time();
      snprintf(buffer, sizeof(buffer), "%llu", time);
      client_send.write(buffer);
      delay(10);
    }
    client_send.stop(); // Close the WiFiClient and release associated resources
    Serial.println("[SEND] DAQ-RPI Connection Reset");
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
      Serial.println("[RECV] Waiting for DAQ-RPI to Connect");
      client_recv = server.available();
      delay(100);
    }
    Serial.println("[RECV] DAQ-RPI Connection Established");
    
    if (client_recv) {
      while (client_recv.connected()) {
        String data = client_recv.readStringUntil('\n');
        if (!data.isEmpty()) {
          Serial.println("[RECV] Received: " + data);
        }
      }
    } else {
      Serial.println("[RECV] DAQ-RPI Connection Reset");
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