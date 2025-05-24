#pragma once

namespace Sensors {
  void init();
  bool readEnv(float& temp, float& humidity);
  bool readPressure(float& pressure);
  bool readCO2(int& eco2, int& tvoc);  // ✅ SGP30
  bool readOutdoor(float &temp, float &hum);  // ✅ logique
  bool motionDetected();
}
