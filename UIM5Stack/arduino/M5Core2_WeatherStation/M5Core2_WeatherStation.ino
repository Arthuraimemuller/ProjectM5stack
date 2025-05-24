#include <M5Unified.h>
#include "ui.h"
#include "sensors.h"
#include "network.h"
#include "utils.h"

unsigned long lastSendTime = 0;
unsigned long lastForecastTime = 0;
ForecastData forecastCache[7];

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  M5.Display.setRotation(1);
  initUI();
  initSensors();
  initRTC();
  connectWiFi();

  getForecast(forecastCache);  // Initial fetch
}

void loop() {
  M5.update();
  updateTimeLabel();

  if (readPIR()) {
    updateHello(true);
  } else {
    updateHello(false);
  }

  float temp, humidity;
  if (readENV(temp, humidity)) {
    updateIndoor(temp, humidity);

    if (millis() - lastSendTime > 60000) {
      sendToBigQuery(temp, humidity);
      lastSendTime = millis();
    }
  }

  float eco2, tvoc;
  if (readSGP30(eco2, tvoc)) {
    updateCO2(eco2);
  }

  float outdoorTemp;
  if (getCurrentWeather(outdoorTemp)) {
    updateOutdoor(outdoorTemp);
  }

  if (millis() - lastForecastTime > 1800000) {
    getForecast(forecastCache);
    lastForecastTime = millis();
  }
  updateForecast(forecastCache);

  delay(1000);
}
