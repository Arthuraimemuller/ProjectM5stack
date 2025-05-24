// #include <M5Unified.h>
// #include <cmath>
// #include <vector>

// namespace Pages {

// struct Point {
//   int x;
//   int y;
//   Point(int x_, int y_) : x(x_), y(y_) {}
// };

// static constexpr int cx = 160;
// static constexpr int cy = 120;
// static constexpr int base_radius = 50;
// static constexpr int num_points = 100;

// static float t = 0.0f;
// static float angle_offset = 0.0f;
// static float valeur = 20.0f;
// static std::vector<Point> old_points;

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

// void drawAnimatedTempPage() {
//   // Efface l'ancien cercle
//   if (!old_points.empty()) {
//     for (size_t i = 0; i < old_points.size(); ++i) {
//       const auto& p1 = old_points[i];
//       const auto& p2 = old_points[(i + 1) % old_points.size()];
//       M5.Display.drawLine(p1.x, p1.y, p2.x, p2.y, TFT_BLACK);
//     }
//   }

//   // Calcule et dessine le nouveau cercle
//   auto points = get_radial_points(t, angle_offset);
//   for (size_t i = 0; i < points.size(); ++i) {
//     const auto& p1 = points[i];
//     const auto& p2 = points[(i + 1) % points.size()];
//     M5.Display.drawLine(p1.x, p1.y, p2.x, p2.y, TFT_BLUE);
//   }

//   old_points = points;

//   float vitesse = get_vitesse(valeur);
//   t += vitesse;
//   //angle_offset += 0.01f;
//   valeur = std::fmod(valeur + 0.1f, 100.0f);
// }

// } // namespace Pages

#include <M5Unified.h>
#include <cmath>
#include <vector>
#include <cstdlib>  // pour std::rand

namespace Pages {

struct Point {
  int x;
  int y;
  Point(int x_, int y_) : x(x_), y(y_) {}
};

static constexpr int cx = 160;
static constexpr int cy = 120;
static constexpr int base_radius = 50;
static constexpr int num_points = 100;

static float t = 0.0f;
static float valeur = 20.0f;
static std::vector<Point> old_points;

std::vector<Point> get_radial_points() {
  std::vector<Point> points;
  for (int i = 0; i < num_points; ++i) {
    float angle = (2 * M_PI / num_points) * i;

    // Déformation aléatoire (valeur entre -10 et +10)
    float deformation = 10.0f * ((std::rand() % 200 - 100) / 100.0f);

    float radius = base_radius + deformation;
    int x = static_cast<int>(cx + radius * std::cos(angle));
    int y = static_cast<int>(cy + radius * std::sin(angle));
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

void drawAnimatedTempPage() {
  // Efface l'ancien tracé
  if (!old_points.empty()) {
    for (size_t i = 0; i < old_points.size(); ++i) {
      const auto& p1 = old_points[i];
      const auto& p2 = old_points[(i + 1) % old_points.size()];
      M5.Display.drawLine(p1.x, p1.y, p2.x, p2.y, TFT_BLACK);
    }
  }

  // Nouveau tracé
  auto points = get_radial_points();
  for (size_t i = 0; i < points.size(); ++i) {
    const auto& p1 = points[i];
    const auto& p2 = points[(i + 1) % points.size()];
    M5.Display.drawLine(p1.x, p1.y, p2.x, p2.y, TFT_BLUE);
  }

  old_points = points;

  float vitesse = get_vitesse(valeur);
  t += vitesse;
  valeur = std::fmod(valeur + 0.1f, 100.0f);
}

} // namespace Pages
