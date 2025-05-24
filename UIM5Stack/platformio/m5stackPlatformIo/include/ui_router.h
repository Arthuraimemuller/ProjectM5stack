#pragma once

enum Page {
  PAGE_HOME,
  PAGE_SETTINGS,
  PAGE_DISPLAY1
};

Page getPageLeft(Page page);
Page getPageRight(Page page);
Page getPageUp(Page page);
Page getPageDown(Page page);

void drawPage(Page page);
void updatePage(Page page);
bool handlePageTouch(Page page, int x, int y);
