#pragma once
#include <M5Unified.h>

class Label {
public:
    Label() : x(0), y(0), text(""), size(1), color(WHITE), font(&fonts::Font2) {}

    void setPosition(int x_, int y_) {
        x = x_;
        y = y_;
    }

    void setTextSize(int s) {
        size = s;
    }

    void setTextColor(uint32_t c) {
        color = c;
    }

    void setFont(const lgfx::IFont* f) {
        font = f;
    }

    void setText(const String& t) {
        // Ne redessine que si le texte a changé
        if (t != text) {
            clear();        // Efface l'ancien texte
            text = t;
            draw();         // Affiche le nouveau
        }
    }

    void draw() {
        if (font) M5.Display.setFont(font);
        M5.Display.setTextSize(size);
        M5.Display.setTextColor(color);
        M5.Display.setCursor(x, y);
        M5.Display.print(text);
    }

private:
    int x, y;
    String text;
    int size;
    uint32_t color;
    const lgfx::IFont* font;

    void clear() {
        if (font) M5.Display.setFont(font);
        int w = M5.Display.textWidth(text);
        int h = M5.Display.fontHeight();
        M5.Display.fillRect(x, y, w, h, BLACK);
    }
};
