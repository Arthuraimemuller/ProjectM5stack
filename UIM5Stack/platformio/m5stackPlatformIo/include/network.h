#pragma once
#include <Arduino.h>
#include <vector>
#include <utility>

namespace Network {
  void init();
  bool isConnected();  // ✅ ajouté
  bool getOutdoorWeather(float& temp, float& humidity);
  bool getForecast(std::vector<std::pair<String, String>>& forecast);
  bool sendToBigQuery(float temp, float humidity);
}

