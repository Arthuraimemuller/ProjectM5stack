#pragma once
#include <M5Unified.h>
#include <Adafruit_SGP30.h>

Adafruit_SGP30 sgp;

bool initSensors() {
  Wire.begin();
  return sgp.begin();
}

bool readENV(float &temp, float &humidity) {
  temp = M5.Env.getTemp();
  humidity = M5.Env.getHum();
  return true;
}

bool readSGP30(float &eco2, float &tvoc) {
  if (sgp.IAQmeasure()) {
    eco2 = sgp.eCO2;
    tvoc = sgp.TVOC;
    return true;
  }
  return false;
}

bool readPIR() {
  return digitalRead(36); // Port B = GPIO36
}
