#include "sensors.h"
#include "M5UnitENV.h"
#include <Adafruit_SGP30.h>
Adafruit_SGP30 sgp;

SHT3X sht3x;
BMP280 bmp;

int pirPin = 36;

void Sensors::init()
{
  Wire.begin(); // Important !
  sht3x.begin(&Wire, SHT3X_I2C_ADDR, 32, 33, 400000U);
  bmp.begin(&Wire, BMP280_I2C_ADDR, 32, 33, 400000U);
  bmp.setSampling(
      BMP280::MODE_NORMAL,
      BMP280::SAMPLING_X2,
      BMP280::SAMPLING_X16,
      BMP280::FILTER_X16,
      BMP280::STANDBY_MS_500);
  pinMode(pirPin, INPUT_PULLDOWN);
  if (!sgp.begin())
  {
    Serial.println("SGP30 sensor not found :(");
  }
  else
  {
    Serial.println("SGP30 sensor initialized.");
  }
}

bool Sensors::readEnv(float &temp, float &hum)
{
  if (!sht3x.update())
    return false;
  temp = sht3x.cTemp;
  hum = sht3x.humidity;
  return true;
}

bool Sensors::readPressure(float &pressure)
{
  if (!bmp.update())
    return false;
  pressure = bmp.pressure; // en Pa
  return true;
}

bool Sensors::readCO2(int &eco2, int &tvoc)
{
  if (sgp.IAQmeasure())
  {
    eco2 = sgp.eCO2;
    tvoc = sgp.TVOC;
    return true;
  }
  return false;
}

bool Sensors::motionDetected()
{
  return digitalRead(pirPin) == HIGH;
}
