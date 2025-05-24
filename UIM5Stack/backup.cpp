// #include <M5Unified.h>
// #include "ui.h"
// #include "sensors.h"
// #include "network.h"
// #include "utils.h"

// unsigned long lastForecastUpdate = 0;
// unsigned long lastSendTime = 0;
// std::vector<std::pair<String, String>> forecastCache(7);

// void setup() {
//   auto cfg = M5.config();
//   M5.begin(cfg);

//   UI::init();
//   Sensors::init();
//   Network::init();
//   Utils::initTime();

//   Serial.begin(115200);  // Optional: for debugging
// }

// void loop() {
//   M5.update();
//   UI::updateTime();

//   // Indoor environment
//   float tempIn, humidity;
//   if (Sensors::readEnv(tempIn, humidity)) {
//     UI::setIndoor(tempIn, humidity);

//     if (millis() - lastSendTime > 60000) {
//       Network::sendToBigQuery(tempIn, humidity);
//       lastSendTime = millis();
//     }
//   } else {
//     UI::setIndoor(NAN, NAN);
//   }

//   // Outdoor weather from API
//   float tempOut, humOut;
//   if (Network::getOutdoorWeather(tempOut, humOut)) {
//     UI::setOutdoor(tempOut);
//   } else {
//     UI::setOutdoor(NAN);
//   }

//   // CO2 / TVOC (SCD4X or simulated)
//   int eco2, tvoc;
//   if (Sensors::readCO2(eco2, tvoc)) {
//     UI::setCO2(eco2);
//   } else {
//     UI::setCO2(-1);
//   }

//   // Motion detection (PIR)
//   UI::showHello(Sensors::motionDetected());

//   // Forecast update every 30 minutes
//   if (millis() - lastForecastUpdate > 30 * 60 * 1000 || forecastCache.empty()) {
//     Network::getForecast(forecastCache);
//     lastForecastUpdate = millis();
//   }

//   // Display forecast on screen
//   for (int i = 0; i < 7 && i < forecastCache.size(); ++i) {
//     UI::setForecast(i, forecastCache[i].first.c_str(), forecastCache[i].second.c_str());
//   }

//   delay(1000);
// }


//MAIN "_______---------------------------------------------------------------------------------------------------------"



// #include <M5Unified.h>
// #include "ui.h"
// #include "sensors.h"
// #include "utils.h"
// #include <LittleFS.h>

// unsigned long lastForecastUpdate = 0;
// unsigned long lastSendTime = 0;
// std::vector<std::pair<String, String>> forecastCache(7);

// void listFontFiles()
// {
//   Serial.println("📁 Vérification des fichiers dans /fonts :");
//   File root = LittleFS.open("/fonts");
//   if (!root || !root.isDirectory())
//   {
//     Serial.println("❌ Le dossier /fonts n'existe pas ou n'est pas un dossier !");
//     return;
//   }

//   File file = root.openNextFile();
//   while (file)
//   {
//     Serial.print(" - ");
//     Serial.println(file.name());
//     file = root.openNextFile();
//   }
// }

// void setup()
// {
//   Serial.begin(115200);
//   auto cfg = M5.config();
//   M5.begin(cfg);

//   // Init filesystem
//   if (!LittleFS.begin())
//   {
//     Serial.println("❌ LittleFS init failed !");
//   }
//   else
//   {
//     Serial.println("✅ LittleFS init OK");
//     listFontFiles();
//   }

//   // Test police .vlw
//   if (M5.Display.loadFont("/fonts/FreeSans14pt.vlw"))
//   {
//     M5.Display.setCursor(10, 30);
//     M5.Display.setTextColor(GREEN);
//     M5.Display.println("✅ Police 14pt chargée !");
//   }
//   else
//   {
//     M5.Display.setCursor(10, 30);
//     M5.Display.setTextColor(RED);
//     M5.Display.println("❌ Erreur chargement police 14pt");
//   }

//   UI::init();
//   Sensors::init();
//   Utils::initTime();
// }

// void loop()
// {
//   M5.update();
//   UI::updateTime();

//   float tempIn, humidity;
//   if (Sensors::readEnv(tempIn, humidity))
//   {
//     UI::setIndoor(tempIn, humidity);
//   }
//   else
//   {
//     UI::setIndoor(NAN, NAN);
//   }

//   float tempOut = 15.0 + random(-30, 30) * 0.1;
//   UI::setOutdoor(tempOut);

//   int eco2, tvoc;
//   if (Sensors::readCO2(eco2, tvoc))
//   {
//     UI::setCO2(eco2);
//   }
//   else
//   {
//     UI::setCO2(-1);
//   }

//   UI::showHello(Sensors::motionDetected());

//   if (millis() - lastForecastUpdate > 30 * 60 * 1000 || forecastCache.empty())
//   {
//     forecastCache.clear();
//     for (int i = 0; i < 7; ++i)
//     {
//       String day = "Day " + String(i + 1);
//       String temp = String(14 + i) + "°C";
//       forecastCache.emplace_back(day, temp);
//     }
//     lastForecastUpdate = millis();
//   }

//   for (int i = 0; i < 3 && i < forecastCache.size(); ++i)
//   {
//     UI::setForecast(i, forecastCache[i].first.c_str(), forecastCache[i].second.c_str());
//   }

//   delay(100); //0.1 secondes
// }

//MAIN 3------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


// #include <M5Unified.h>
// #include <LittleFS.h>

// void listFontFiles() {
//   Serial.println("📁 Listing /fonts:");
//   File root = LittleFS.open("/fonts");
//   if (!root || !root.isDirectory()) {
//     Serial.println("❌ Le dossier /fonts n'existe pas !");
//     return;
//   }

//   File file = root.openNextFile();
//   while (file) {
//     Serial.print(" - ");
//     Serial.println(file.name());
//     file = root.openNextFile();
//   }
// }

// void setup() {
//   Serial.begin(115200);
//   delay(100);  // Laisse le temps à la console série de s'initialiser

//   auto cfg = M5.config();
//   M5.begin(cfg);

//   M5.Display.setTextColor(WHITE, BLACK);
//   M5.Display.setCursor(10, 10);
//   M5.Display.clear(BLACK);

//   // Initialisation du système de fichiers
//   if (!LittleFS.begin()) {
//     Serial.println("❌ LittleFS init failed");
//     M5.Display.setTextColor(RED, BLACK);
//     M5.Display.println("LittleFS failed");
//     return;
//   }

//   Serial.println("✅ LittleFS init OK");
//   listFontFiles();

//   const char* fontPath = "/fonts/FreeSans18pt.vlw";

//   // Vérifie si le fichier existe avant de tenter de le charger
//   if (!LittleFS.exists(fontPath)) {
//     M5.Display.setTextColor(RED, BLACK);
//     M5.Display.println("❌ Fichier manquant : FreeSans18pt.vlw");
//     Serial.println("❌ Fichier .vlw non trouvé sur LittleFS");
//     return;
//   }

//   // Test de chargement de la police
//   if (M5.Display.loadFont(fontPath)) {
//     M5.Display.setFont(M5.Display.getFont());
//     M5.Display.setCursor(40, 60);
//     M5.Display.setTextColor(WHITE, BLACK);
//     M5.Display.println("Température : 23°C");
//     Serial.println("✅ Police chargée et ° affiché");
//   } else {
//     M5.Display.setTextColor(RED, BLACK);
//     M5.Display.setCursor(40, 60);
//     M5.Display.println("Erreur police .vlw");
//     Serial.println("❌ Échec chargement police");
//   }
// }

// void loop() {
//   // rien
// }

//main4------------------------------------------------------------------------------------------------------------------------------------------
// #include <M5Unified.h>
// //#include "NotoSans18pt.h"  // Assure-toi que ce fichier est dans ton dossier `include/` ou `src/`

// void setup() {
//   Serial.begin(115200);
//   delay(100);  // Laisse le temps à la console série de s'initialiser

//   auto cfg = M5.config();
//   M5.begin(cfg);

//   M5.Display.setTextColor(WHITE, BLACK);
//   M5.Display.setCursor(10, 10);
//   M5.Display.clear(BLACK);

//   // Utilisation directe de la police embarquée
//   M5.Display.setFont(&fonts::FreeSansBoldOblique12pt7b);  // 💡 Remplace par le nom exact dans le fichier .h
//   M5.Display.setCursor(40, 60);
//   M5.Display.println("Température : 23°C");
//   Serial.println("✅ Police NotoSans chargée depuis .h");
// }

// void loop() {
//   // rien
// }


// main --------------------------------------------------------------------------------------------------------------
// #include <M5Unified.h>

// M5Canvas canvas(&M5.Display);
// int angle = 0;

// void setup() {
//   M5.begin();
//   canvas.createSprite(320, 240);         // taille de la zone animée
//   canvas.setTextColor(WHITE);
//   canvas.setFont(&fonts::Font0);
// }

// void loop() {
//   M5.update();

//   // Efface le canvas (pas l’écran)
//   canvas.fillSprite(BLACK);

//   // Calcul de la position X en oscillation (cosinus)
//   int x = 160 + 50 * cos(angle * DEG_TO_RAD);
//   int y = 120;

//   // Dessine un cercle à la position calculée
//   canvas.fillCircle(x, y, 20, GREEN);

//   // Affiche sur l’écran
//   canvas.pushSprite(0, 0);

//   // Incrémente l’angle
//   angle = (angle + 5) % 360;

//   delay(30);  // ralentir un peu l’animation
// }
// -----------------------------
// Version SANS CANVAS
// -----------------------------
// #include <M5Unified.h>
// #include <cmath>
// #include <vector>

// struct Point {
//   int x;
//   int y;
//   Point(int x_, int y_) : x(x_), y(y_) {}
// };

// constexpr int cx = 160;
// constexpr int cy = 120;
// constexpr int base_radius = 50;
// constexpr int num_points = 100;

// float t = 0.0f;
// float angle_offset = 0.0f;
// float valeur = 20.0f;

// std::vector<Point> old_points;

// std::vector<Point> get_radial_points(float t, float angle_offset) {
//   std::vector<Point> points;
//   float osc = std::sin(t);
//   for (int i = 0; i < num_points; ++i) {
//     float angle = (2 * M_PI / num_points) * i;
//     float deformation = 10 * osc * std::sin(5 * angle + t);
//     float radius = base_radius + deformation;
//     int x = static_cast<int>(cx + radius * std::cos(angle + angle_offset));
//     int y = static_cast<int>(cy + radius * std::sin(angle + angle_offset));
//     points.emplace_back(x, y);
//   }
//   return points;
// }

// float get_vitesse(float valeur) {
//   float min_v = 0.005f;
//   float max_v = 0.1f;
//   float seuil = 37.0f;
//   if (valeur <= seuil) {
//     float norm = std::min(std::max(valeur / seuil, 0.0f), 1.0f);
//     return min_v + norm * (max_v - min_v);
//   } else {
//     float k = 0.1f;
//     float exp_val = max_v * std::exp(k * (valeur - seuil));
//     return std::min(exp_val, 1.0f);
//   }
// }

// void setup() {
//   auto cfg = M5.config();
//   M5.begin(cfg);
//   M5.Display.clear();
//   M5.Display.setColor(TFT_BLUE);
// }

// void loop() {
//   if (!old_points.empty()) {
//     for (size_t i = 0; i < old_points.size(); ++i) {
//       auto& p1 = old_points[i];
//       auto& p2 = old_points[(i + 1) % old_points.size()];
//       M5.Display.drawLine(p1.x, p1.y, p2.x, p2.y, TFT_BLACK);
//     }
//   }

//   auto points = get_radial_points(t, angle_offset);
//   for (size_t i = 0; i < points.size(); ++i) {
//     auto& p1 = points[i];
//     auto& p2 = points[(i + 1) % points.size()];
//     M5.Display.drawLine(p1.x, p1.y, p2.x, p2.y, TFT_BLUE);
//   }

//   old_points = points;

//   float vitesse = get_vitesse(valeur);
//   t += vitesse;
//   angle_offset += 0.01f;
//   valeur = std::fmod(valeur + 0.1f, 100.0f);

//   delay(30);
// }
//main (display swipe, yes!!!!)---------------------------------------------------------------------------------------------------------------------------------------------------------------------
// #include <M5Unified.h>
// #include "ui_pages.h"

// Page currentPage = PAGE_HOME;

// void setup() {
//   auto cfg = M5.config();
//   M5.begin(cfg);
//   M5.Display.setTextColor(WHITE);
//   M5.Display.setTextDatum(middle_center);
//   M5.Display.setFont(&fonts::Font0);
//   M5.Display.clear(BLACK);
//   drawPage(currentPage);
// }

// void loop() {
//   M5.update();
//   static int last_x = 0, last_y = 0;

//   if (M5.Touch.getCount() > 0) {
//     auto t = M5.Touch.getDetail();

//     if (t.wasPressed()) {
//       last_x = t.x;
//       last_y = t.y;
//     }

//     if (t.wasReleased()) {
//       int dx = t.x - last_x;
//       int dy = t.y - last_y;

//       if (std::abs(dx) > 50 || std::abs(dy) > 50) {
//         Page newPage = currentPage;
//         if (std::abs(dx) > std::abs(dy)) {
//           newPage = (dx > 0) ? getPageRight(currentPage) : getPageLeft(currentPage);
//         } else {
//           newPage = (dy > 0) ? getPageDown(currentPage) : getPageUp(currentPage);
//         }

//         if (newPage != currentPage) {
//           currentPage = newPage;
//           drawPage(currentPage);
//         }
//       }

//       // test click action
//       if (handlePageTouch(currentPage, t.x, t.y)) {
//         drawPage(currentPage);
//       }
//     }
//   }

//   delay(20);
// }


#include <M5Unified.h>
#include "ui/ui_router.h"

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

      if (handlePageTouch(currentPage, t.x, t.y)) {
        drawPage(currentPage);
      }
    }
  }

  delay(20);
}
