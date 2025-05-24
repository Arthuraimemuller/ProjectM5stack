 #include <M5Unified.h>
 #include <cmath>
 #include <vector>

 struct Point {
   int x;
   int y;
   Point(int x_, int y_) : x(x_), y(y_) {}
 };

 constexpr int cx = 160;
 constexpr int cy = 120;
 constexpr int base_radius = 50;
 constexpr int num_points = 100;

 float t = 0.0f;
 float angle_offset = 0.0f;
 float valeur = 20.0f;

 std::vector<Point> old_points;

 std::vector<Point> get_radial_points(float t, float angle_offset) {
   std::vector<Point> points;
   float osc = std::sin(t);
   for (int i = 0; i < num_points; ++i) {
     float angle = (2 * M_PI / num_points) * i;
     float deformation = 10 * osc * std::sin(5 * angle + t);
     float radius = base_radius + deformation;
     int x = static_cast<int>(cx + radius * std::cos(angle + angle_offset));
     int y = static_cast<int>(cy + radius * std::sin(angle + angle_offset));
     points.emplace_back(x, y);
   }
   return points;
 }

 float get_vitesse(float valeur) {
   float min_v = 0.005f;
   float max_v = 0.1f;
   float seuil = 37.0f;
   if (valeur <= seuil) {
     float norm = std::min(std::max(valeur / seuil, 0.0f), 1.0f);
     return min_v + norm * (max_v - min_v);
   } else {
     float k = 0.1f;
     float exp_val = max_v * std::exp(k * (valeur - seuil));
     return std::min(exp_val, 1.0f);
   }
 }

 void setup() {
   auto cfg = M5.config();
   M5.begin(cfg);
   M5.Display.clear();
   M5.Display.setColor(TFT_BLUE);
 }

 void loop() {
   if (!old_points.empty()) {
     for (size_t i = 0; i < old_points.size(); ++i) {
       auto& p1 = old_points[i];
       auto& p2 = old_points[(i + 1) % old_points.size()];
       M5.Display.drawLine(p1.x, p1.y, p2.x, p2.y, TFT_BLACK);
     }
   }

   auto points = get_radial_points(t, angle_offset);
   for (size_t i = 0; i < points.size(); ++i) {
     auto& p1 = points[i];
     auto& p2 = points[(i + 1) % points.size()];
     M5.Display.drawLine(p1.x, p1.y, p2.x, p2.y, TFT_BLUE);
   }

   old_points = points;

   float vitesse = get_vitesse(valeur);
   t += vitesse;
   angle_offset += 0.01f;
   valeur = std::fmod(valeur + 0.1f, 100.0f);

   delay(30);
 }