#pragma once
#include <M5Unified.h>
#include "Label.h"

namespace UI {

  // Déclare les composants
  extern Label labelDateTime;
  extern Label labelIndoor;
  extern Label labelOutdoor;
  extern Label labelCO2;
  extern Label labelHello;
  extern Label labelDebug;
  extern Label forecastDays[3];
  extern Label forecastTemps[3];

  // Fonctions principales
  void initLayout();     // Appelé une fois par page
  void updateData();     // Appelé régulièrement (toutes les secondes)

  // Outils communs
  void drawButton(int x, int y, int w, int h, const String& text, uint32_t bgColor, uint32_t textColor);
  void updateTime();
  void showHello(bool active);
  void setIndoor(float temp, float hum);
  void setOutdoor(float temp);
  void setCO2(int ppm);
  void setForecast(int i, const char* day, const char* temp);
  void showDebug(const char* msg);
}
