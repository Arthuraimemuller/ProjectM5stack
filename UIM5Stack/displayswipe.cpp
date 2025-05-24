#include <M5Unified.h>
#include "ui_pages.h"

Page currentPage = PAGE_HOME;

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  M5.Display.setTextColor(WHITE);
  M5.Display.setTextDatum(middle_center);
  M5.Display.setFont(&fonts::Font0);
  M5.Display.clear(BLACK);
  drawPage(currentPage);
}

void loop() {
  M5.update();
  static int last_x = 0, last_y = 0;

  if (M5.Touch.getCount() > 0) {
    auto t = M5.Touch.getDetail();

    if (t.wasPressed()) {
      last_x = t.x;
      last_y = t.y;
    }

    if (t.wasReleased()) {
      int dx = t.x - last_x;
      int dy = t.y - last_y;

      if (std::abs(dx) > 50 || std::abs(dy) > 50) {
        Page newPage = currentPage;
        if (std::abs(dx) > std::abs(dy)) {
          newPage = (dx > 0) ? getPageRight(currentPage) : getPageLeft(currentPage);
        } else {
          newPage = (dy > 0) ? getPageDown(currentPage) : getPageUp(currentPage);
        }

        if (newPage != currentPage) {
          currentPage = newPage;
          drawPage(currentPage);
        }
      }

      // test click action
      if (handlePageTouch(currentPage, t.x, t.y)) {
        drawPage(currentPage);
      }
    }
  }

  delay(20);
}