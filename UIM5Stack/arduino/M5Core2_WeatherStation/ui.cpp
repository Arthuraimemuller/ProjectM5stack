#include "ui.h"

M5Canvas canvas(&M5.Display);

M5Label labelDateTime;
M5Label labelIndoor;
M5Label labelOutdoor;
M5Label labelCO2;
M5Label labelHello;

M5Label forecastDays[7];
M5Label forecastTemps[7];

void initUI() {
  M5.Display.clear(BLACK);

  canvas.createSprite(M5.Display.width(), M5.Display.height());
  canvas.fillSprite(BLACK);

  labelDateTime.create(&canvas, 50, 5, 1, "");
  labelDateTime.setTextColor(WHITE);

  labelIndoor.create(&canvas, 20, 75, 1, "-- °C\n-- %");
  labelIndoor.setTextColor(WHITE);

  labelOutdoor.create(&canvas, 125, 90, 1, "-- °C");
  labelOutdoor.setTextColor(WHITE);

  labelCO2.create(&canvas, 225, 90, 1, "-- ppm");
  labelCO2.setTextColor(WHITE);

  labelHello.create(&canvas, 220, 10, 1, "");
  labelHello.setTextColor(WHITE);

  int start_x = 10;
  int gap_x = 40;
  for (int i = 0; i < 7; i++) {
    forecastDays[i].create(&canvas, start_x + i * gap_x, 140, 1, "---");
    forecastDays[i].setTextColor(WHITE);

    forecastTemps[i].create(&canvas, start_x + i * gap_x, 160, 1, "-- °C");
    forecastTemps[i].setTextColor(WHITE);
  }

  // Affichage des images (attention: SD doit être monté)
  M5.Display.drawPngFile(SD, "/res/home_imresizer.png", 40, 45);
  M5.Display.drawPngFile(SD, "/res/outdoor_imresizer.png", 140, 45);
  M5.Display.drawPngFile(SD, "/res/co2_imresizer.png", 245, 45);
  M5.Display.drawPngFile(SD, "/res/weatherIcon_imresizer.png", 0, 0);
}

void updateTimeLabel() {
  auto t = M5.Rtc.getDateTime();
  char buf[32];
  sprintf(buf, "%04d-%02d-%02d %02d:%02d:%02d",
          t.date.year, t.date.month, t.date.day,
          t.time.hours, t.time.minutes, t.time.seconds);
  labelDateTime.setText(buf);
}

void updateIndoor(float t, float h) {
  char buf[32];
  sprintf(buf, "%.1f °C\n%.0f %%", t, h);
  labelIndoor.setText(buf);
}

void updateOutdoor(float t) {
  char buf[16];
  sprintf(buf, "%.1f °C", t);
  labelOutdoor.setText(buf);
}

void updateCO2(float ppm) {
  char buf[16];
  sprintf(buf, "%.0f ppm", ppm);
  labelCO2.setText(buf);
}

void updateHello(bool detected) {
  labelHello.setText(detected ? "Hello" : "");
}

void updateForecast(ForecastData forecast[7]) {
  for (int i = 0; i < 7; i++) {
    forecastDays[i].setText(forecast[i].day);
    forecastTemps[i].setText(forecast[i].temp);
  }
}
