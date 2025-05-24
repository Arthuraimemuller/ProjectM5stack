#include "ui_router.h"
#include "pages/home_page.h"
#include "pages/settings_page.h"
#include "pages/animated_temp_page.h"
#include <M5Unified.h>

using namespace Pages;

Page getPageLeft(Page page) {
  if (page == PAGE_DISPLAY1) return PAGE_HOME;
  return page;
}

Page getPageRight(Page page) {
  if (page == PAGE_HOME) return PAGE_DISPLAY1;
  return page;
}

Page getPageUp(Page /*page*/) {
  return PAGE_HOME;
}

Page getPageDown(Page /*page*/) {
  return PAGE_SETTINGS;
}

void drawPage(Page page) {
  // 🧠 Efface l’écran au changement de page (mais pas dans updatePage)
  M5.Display.clear(TFT_BLACK);

  switch (page) {
    case PAGE_HOME:
      drawHomePage(); break;
    case PAGE_SETTINGS:
      drawSettingsPage(); break;
    case PAGE_DISPLAY1:
      drawAnimatedTempPage(); break;
  }
}

bool handlePageTouch(Page page, int x, int y) {
  // À personnaliser si tu veux ajouter des boutons tactiles par page
  return false;
}

void updatePage(Page page) {
  // ⚠️ Ne pas effacer l’écran ici ! Juste mettre à jour les données dynamiques
  switch (page) {
    case PAGE_DISPLAY1:
      drawAnimatedTempPage();  // animation continue
      break;

    case PAGE_HOME:
      // 🧠 ne rappelle pas drawHomePage() si elle efface l’écran à chaque fois
      // À la place, appelle UI::updateData() dans home_page.cpp
      break;

    default:
      break;
  }
}
