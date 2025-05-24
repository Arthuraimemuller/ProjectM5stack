#pragma once
#include <M5Unified.h>

// Canvas sur toute la surface de l'écran
extern M5Canvas canvas;

extern M5Label labelDateTime;
extern M5Label labelIndoor;
extern M5Label labelOutdoor;
extern M5Label labelCO2;
extern M5Label labelHello;

extern M5Label forecastDays[7];
extern M5Label forecastTemps[7];

void initUI();
void updateTimeLabel();
void updateIndoor(float t, float h);
void updateOutdoor(float t);
void updateCO2(float ppm);
void updateHello(bool detected);

struct ForecastData {
  const char* day;
  const char* temp;
};

void updateForecast(ForecastData forecast[7]);
