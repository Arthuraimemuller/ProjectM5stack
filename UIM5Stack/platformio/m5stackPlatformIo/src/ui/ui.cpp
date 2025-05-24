#include "ui.h"
#include "utils.h"
#include "sensors.h"
#include "network.h"

// Définition des labels (extern)
namespace UI {
  M5Canvas canvas;

  Label labelDateTime;
  Label labelIndoor;
  Label labelOutdoor;
  Label labelCO2;
  Label labelHello;
  Label labelDebug;
  Label forecastDays[3];
  Label forecastTemps[3];

  void drawButton(int x, int y, int w, int h, const String& text, uint32_t bgColor, uint32_t textColor) {
    M5.Display.fillRoundRect(x, y, w, h, 8, bgColor);
    M5.Display.setFont(&fonts::Font2);
    M5.Display.setTextColor(textColor, bgColor);
    int tw = M5.Display.textWidth(text);
    int th = M5.Display.fontHeight();
    int tx = x + (w - tw) / 2;
    int ty = y + (h - th) / 2;
    M5.Display.setCursor(tx, ty);
    M5.Display.print(text);
  }

  void initLayout() {
    M5.Display.clear(TFT_BLACK);

    const lgfx::IFont* fontSmall = &fonts::Font0;
    const lgfx::IFont* fontMedium = &fonts::Font2;
    const lgfx::IFont* fontLarge = &fonts::Font4;

    labelDateTime.setFont(fontMedium);
    labelDateTime.setPosition(10, 5);
    labelDateTime.setTextColor(WHITE);

    drawButton(20, 50, 90, 40, "Indoor", BLUE, WHITE);
    drawButton(120, 50, 90, 40, "Outdoor", GREEN, BLACK);
    drawButton(220, 50, 90, 40, "CO2", RED, WHITE);

    labelIndoor.setFont(fontMedium);
    labelIndoor.setPosition(30, 95);

    labelOutdoor.setFont(fontMedium);
    labelOutdoor.setPosition(130, 95);

    labelCO2.setFont(fontMedium);
    labelCO2.setPosition(230, 95);

    labelDebug.setFont(fontSmall);
    labelDebug.setPosition(10, 200);

    labelHello.setFont(fontLarge);
    labelHello.setPosition(220, 10);
    labelHello.setTextColor(RED);

    for (int i = 0; i < 3; ++i) {
      forecastDays[i].setFont(fontSmall);
      forecastDays[i].setPosition(10 + i * 100, 140);

      forecastTemps[i].setFont(fontSmall);
      forecastTemps[i].setPosition(10 + i * 100, 160);
    }
  }

  void updateTime() {
    labelDateTime.setText(Utils::getDateStr() + " " + Utils::getTimeStr());
  }

  void updateData() {
    updateTime();

    float tempIn, hum;
    if (Sensors::readEnv(tempIn, hum)) setIndoor(tempIn, hum);
    else setIndoor(NAN, NAN);

    float tempOut, humOut;
    if (Network::getOutdoorWeather(tempOut, humOut)) setOutdoor(tempOut);
    else setOutdoor(NAN);

    int eco2, tvoc;
    if (Sensors::readCO2(eco2, tvoc)) setCO2(eco2);
    else setCO2(-1);

    showHello(Sensors::motionDetected());

    setForecast(0, "Mon", "18°C");
    setForecast(1, "Tue", "21°C");
    setForecast(2, "Wed", "17°C");
  }

  void setIndoor(float temp, float hum) {
    if (isnan(temp)) labelIndoor.setText("--\xB0""C\n--%");
    else labelIndoor.setText(String(temp, 1) + "\xB0""C\n" + String(hum, 0) + "%");
  }

  void setOutdoor(float temp) {
    labelOutdoor.setText(isnan(temp) ? "--\xB0""C" : String(temp, 1) + "\xB0""C");
  }

  void setCO2(int ppm) {
    labelCO2.setText(ppm < 0 ? "-- ppm" : String(ppm) + " ppm");
  }

  void showHello(bool active) {
    labelHello.setText(active ? "Hello" : "");
  }

  void setForecast(int i, const char* day, const char* temp) {
    if (i < 0 || i >= 3) return;
    forecastDays[i].setText(day);
    forecastTemps[i].setText(temp);
  }

  void showDebug(const char* msg) {
    labelDebug.setText(msg);
  }

} // namespace UI
