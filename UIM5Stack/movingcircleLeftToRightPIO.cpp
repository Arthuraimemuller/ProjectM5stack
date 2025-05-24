#include <M5Unified.h>

M5Canvas canvas(&M5.Display);
int angle = 0;

void setup() {
  M5.begin();
  canvas.createSprite(320, 240);         // taille de la zone animée
  canvas.setTextColor(WHITE);
  canvas.setFont(&fonts::Font0);
}

void loop() {
  M5.update();

  // Efface le canvas (pas l’écran)
  canvas.fillSprite(BLACK);

  // Calcul de la position X en oscillation (cosinus)
  int x = 160 + 50 * cos(angle * DEG_TO_RAD);
  int y = 120;

  // Dessine un cercle à la position calculée
  canvas.fillCircle(x, y, 20, GREEN);

  // Affiche sur l’écran
  canvas.pushSprite(0, 0);

  // Incrémente l’angle
  angle = (angle + 5) % 360;

  delay(30);  // ralentir un peu l’animation
}
