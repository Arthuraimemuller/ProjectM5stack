#pragma once
#include <M5Unified.h>

enum Page {
  PAGE_HOME,
  PAGE_DISPLAY1,
  PAGE_DISPLAY2,
  PAGE_SETTINGS
};

void drawHomePage() {
  M5.Display.clear(BLACK);
  M5.Display.setTextSize(2);
  M5.Display.drawString("\xF0\x9F\x8F\xA0 Home", 160, 100);
}

void drawDisplay1Page() {
  M5.Display.clear(BLACK);
  M5.Display.setTextSize(2);
  M5.Display.drawString("Display 1", 160, 100);
}

void drawDisplay2Page() {
  M5.Display.clear(BLACK);
  M5.Display.setTextSize(2);
  M5.Display.drawString("Display 2", 160, 100);
}

void drawSettingsPage() {
  M5.Display.clear(BLACK);
  M5.Display.setTextSize(2);
  M5.Display.drawString("\xE2\x9A\x99 Settings", 160, 100);
}

void drawPage(Page page) {
  switch (page) {
    case PAGE_HOME: drawHomePage(); break;
    case PAGE_DISPLAY1: drawDisplay1Page(); break;
    case PAGE_DISPLAY2: drawDisplay2Page(); break;
    case PAGE_SETTINGS: drawSettingsPage(); break;
  }
}

Page getPageLeft(Page page) {
  if (page == PAGE_DISPLAY2) return PAGE_DISPLAY1;
  if (page == PAGE_DISPLAY1) return PAGE_HOME;
  return page;
}

Page getPageRight(Page page) {
  if (page == PAGE_HOME) return PAGE_DISPLAY1;
  if (page == PAGE_DISPLAY1) return PAGE_DISPLAY2;
  return page;
}

Page getPageUp(Page page) {
  return PAGE_HOME;
}

Page getPageDown(Page page) {
  return PAGE_SETTINGS;
}

bool handlePageTouch(Page page, int x, int y) {
  // ici tu peux ajouter des "boutons invisibles" par page
  if (page == PAGE_HOME && x > 100 && y > 180 && y < 220) {
    M5.Display.drawString("Home pressed zone", 160, 200);
    return true;
  }
  return false;
}
