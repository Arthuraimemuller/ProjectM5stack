#pragma once
#include <M5Unified.h>

void initRTC() {
  M5.Rtc.setTimeZone(2 * 3600); // GMT+2
  M5.Rtc.begin();
  M5.Rtc.setDateTimeFromNTP("pool.ntp.org");
}

String getCurrentDate() {
  auto t = M5.Rtc.getDateTime();
  char buf[16];
  sprintf(buf, "%04d-%02d-%02d", t.date.year, t.date.month, t.date.day);
  return String(buf);
}

String getCurrentTime() {
  auto t = M5.Rtc.getDateTime();
  char buf[16];
  sprintf(buf, "%02d:%02d:%02d", t.time.hours, t.time.minutes, t.time.seconds);
  return String(buf);
}
