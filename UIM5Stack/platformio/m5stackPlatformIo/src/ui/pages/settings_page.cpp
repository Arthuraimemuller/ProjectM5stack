#include <M5Unified.h>

namespace Pages {

void drawSettingsPage() {
  M5.Display.clear(BLACK);
  M5.Display.setTextSize(2);
  M5.Display.setTextDatum(middle_center);
  M5.Display.drawString("\xE2\x9A\x99 Settings Page", 160, 120);
}

} // namespace Pages
