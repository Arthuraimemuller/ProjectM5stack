#include <M5Unified.h>

#define BTN_CENTER_X 160
#define BTN_CENTER_Y 120
#define BTN_RADIUS   40

bool isInsideCircle(int x, int y, int cx, int cy, int r) {
  int dx = x - cx;
  int dy = y - cy;
  return dx * dx + dy * dy <= r * r;
}

void drawRoundButton(const char* label) {
  M5.Display.fillCircle(BTN_CENTER_X, BTN_CENTER_Y, BTN_RADIUS, TFT_DARKGREY);
  M5.Display.drawCircle(BTN_CENTER_X, BTN_CENTER_Y, BTN_RADIUS, TFT_WHITE);
  M5.Display.setTextDatum(middle_center);
  M5.Display.setTextColor(WHITE);
  M5.Display.setTextSize(2);
  M5.Display.drawString(label, BTN_CENTER_X, BTN_CENTER_Y);
}

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  M5.Display.clear(BLACK);
  drawRoundButton("OK");
}

void loop() {
  M5.update();

  if (M5.Touch.getCount() > 0) {
    auto t = M5.Touch.getDetail();
    if (t.wasPressed()) {
      if (isInsideCircle(t.x, t.y, BTN_CENTER_X, BTN_CENTER_Y, BTN_RADIUS)) {
        M5.Display.fillScreen(BLACK);
        M5.Display.drawString("🎉 Pressed!", BTN_CENTER_X, BTN_CENTER_Y);
        delay(1000);
        M5.Display.clear(BLACK);
        drawRoundButton("OK");
      }
    }
  }

  delay(20);
}
