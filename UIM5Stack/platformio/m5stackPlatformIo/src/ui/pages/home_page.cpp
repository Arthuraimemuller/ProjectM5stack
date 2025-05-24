#include <M5Unified.h>
#include "ui.h"
#include "sensors.h"
#include "utils.h"
#include "network.h"

namespace Pages {

  // Empêche l'initialisation multiple de l'interface
  static bool uiInitialized = false;

  void drawHomePage() {
    if (!uiInitialized) {
      UI::initLayout();      // 🧱 Structure de la page (boutons, labels, etc.)
      uiInitialized = true;
    }

    UI::updateData();        // 🔄 Données temps réel (capteurs, météo, etc.)
  }

} // namespace Pages
