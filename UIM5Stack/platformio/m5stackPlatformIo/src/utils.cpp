#include "utils.h"
#include <WiFi.h>
#include <time.h>

void Utils::initTime() {
  configTime(7200, 0, "pool.ntp.org");
  while (time(nullptr) < 100000) delay(500);
}

String Utils::getDateStr() {
  struct tm timeinfo;
  getLocalTime(&timeinfo);
  char buf[11];
  strftime(buf, sizeof(buf), "%Y-%m-%d", &timeinfo);
  return String(buf);
}

String Utils::getTimeStr() {
  struct tm timeinfo;
  getLocalTime(&timeinfo);
  char buf[9];
  strftime(buf, sizeof(buf), "%H:%M:%S", &timeinfo);
  return String(buf);
}
