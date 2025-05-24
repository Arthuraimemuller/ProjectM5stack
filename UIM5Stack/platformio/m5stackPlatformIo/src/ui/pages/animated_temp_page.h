#pragma once
#include <vector>

namespace Pages {

struct Point {
  int x;
  int y;
  Point(int x_, int y_) : x(x_), y(y_) {}
};

void drawAnimatedTempPage();

} // namespace Pages