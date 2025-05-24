#pragma once
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "utils.h"

const char *ssid = "YOUR_SSID";
const char *password = "YOUR_PASS";
const char *BIGQUERY_URL = "https://.../send-to-bigquery";
const char *BACKEND_WEATHER_CURRENT = "https://.../weather/current";
const char *BACKEND_WEATHER_FORECAST = "https://.../weather/forecast";

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

bool getCurrentWeather(float &temp) {
  HTTPClient http;
  http.begin(BACKEND_WEATHER_CURRENT);
  int code = http.GET();
  if (code == 200) {
    DynamicJsonDocument doc(512);
    deserializeJson(doc, http.getStream());
    temp = doc["temperature"].as<float>();
    http.end();
    return true;
  }
  http.end();
  return false;
}

struct ForecastData {
  char day[4];
  char temp[8];
};

bool getForecast(ForecastData forecast[7]) {
  HTTPClient http;
  http.begin(BACKEND_WEATHER_FORECAST);
  int code = http.GET();
  if (code == 200) {
    DynamicJsonDocument doc(2048);
    deserializeJson(doc, http.getStream());
    http.end();

    const char *days[] = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};
    for (int i = 0; i < 7; i++) {
      if (!doc[i]) break;
      const char *date = doc[i]["date"];
      float tempVal = doc[i]["temp"];
      struct tm tm{};
      strptime(date, "%Y-%m-%d", &tm);
      strncpy(forecast[i].day, days[tm.tm_wday], 4);
      snprintf(forecast[i].temp, 8, "%.1f °C", tempVal);
    }
    return true;
  }
  http.end();
  return false;
}

void sendToBigQuery(float temp, float humidity) {
  HTTPClient http;
  http.begin(BIGQUERY_URL);
  http.addHeader("Content-Type", "application/json");

  DynamicJsonDocument doc(512);
  doc["passwd"] = "943912667b08be19402bfc3a51a921cfc85f794938d4e23a1b7e37013c453f1e";
  JsonObject values = doc.createNestedObject("values");
  values["date"] = getCurrentDate();
  values["time"] = getCurrentTime();
  values["indoor_temp"] = temp;
  values["indoor_humidity"] = humidity;

  String payload;
  serializeJson(doc, payload);
  http.POST(payload);
  http.end();
}
