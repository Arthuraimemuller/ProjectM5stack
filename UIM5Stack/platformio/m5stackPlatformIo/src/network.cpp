#include "network.h"
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>

char ssid[] = "YOUR_SSID";
char password[] = "YOUR_PASSWORD";
const char* weatherCurrentURL = "https://your-backend/weather/current";
const char* forecastURL = "https://your-backend/weather/forecast";
const char* bigQueryURL = "https://your-backend/send-to-bigquery";

void Network::init() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts++ < 20) {
    Serial.print(".");
    delay(500);
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWi-Fi connected");
  } else {
    Serial.println("\nWi-Fi connection failed");
  }
}

bool Network::isConnected() {
  return WiFi.status() == WL_CONNECTED;
}

bool Network::getOutdoorWeather(float& temp, float& humidity) {
  if (!isConnected()) {
    Serial.println("Wi-Fi not connected, skipping weather fetch.");
    return false;
  }

  WiFiClientSecure client;
  client.setInsecure();  // Insecure mode for test/dev only

  HTTPClient http;
  if (!http.begin(client, weatherCurrentURL)) {
    Serial.println("HTTPClient failed to begin HTTPS connection");
    return false;
  }

  int code = http.GET();
  if (code != 200) {
    Serial.printf("GET failed with code %d\n", code);
    http.end();
    return false;
  }

  String payload = http.getString();
  http.end();

  // Simulate parsing
  temp = payload.toFloat();
  humidity = 50.0;  // placeholder
  return true;
}

bool Network::getForecast(std::vector<std::pair<String, String>>& forecast) {
  forecast.clear();
  for (int i = 0; i < 7; ++i)
    forecast.emplace_back("Day", String(15 + i) + "°C");
  return true;
}

bool Network::sendToBigQuery(float temp, float humidity) {
  if (!isConnected()) {
    Serial.println("Wi-Fi not connected, skipping BigQuery send.");
    return false;
  }

  WiFiClientSecure client;
  client.setInsecure();

  HTTPClient http;
  if (!http.begin(client, bigQueryURL)) {
    Serial.println("HTTPClient failed to begin");
    return false;
  }

  http.addHeader("Content-Type", "application/json");
  String payload = String("{\"values\":{\"temp\":") + temp + ",\"hum\":" + humidity + "}}";

  int code = http.POST(payload);
  http.end();

  if (code != 200) {
    Serial.printf("POST failed with code %d\n", code);
    return false;
  }

  return true;
}
