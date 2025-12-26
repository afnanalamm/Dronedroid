#include <LiquidCrystal.h>

// Initialize library with the interface pins
const int rs = 7, en = 8, d4 = 9, d5 = 10, d6 = 11, d7 = 12;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

#define ENABLE1 5
#define ENABLE2 3
#define DIR1 6
#define DIR2 4


const float gravity = 100;

String inputString = "";         // A String to hold incoming data
boolean stringComplete = false;  // Whether the string is complete


void setup() {
  pinMode(ENABLE1, OUTPUT);
  pinMode(ENABLE2, OUTPUT);
  pinMode(DIR1, OUTPUT);
  pinMode(DIR2, OUTPUT);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, HIGH);

  lcd.begin(16, 2);
  Serial.begin(9600);
  inputString.reserve(50);  // Reserve space to avoid fragmentation
  // Serial.setTimeout(10); 

  // lcd.print("Input:");
  lcd.setCursor(0, 1);
}

void loop() {
  if (Serial.available()) {
    serialEvent();

      if (stringComplete) {

        // Expected format: pwm1,pwm2
        float pwm1 = 0;
        float pwm2 = 0;

        int commaIndex = inputString.indexOf(',');

        if (commaIndex > 0) {
          pwm1 = inputString.substring(0, commaIndex).toFloat();
          pwm2 = inputString.substring(commaIndex + 1).toFloat();
        }

        pwm1 = constrain(pwm1, 0, 255);
        pwm2 = constrain(pwm2, 0, 255);

        analogWrite(ENABLE1, (int)pwm1);
        analogWrite(ENABLE2, (int)pwm2);

        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(inputString);

        inputString = "";
        stringComplete = false;
      }


    // Read X and Y as floats: "x,y\n"
    // float x = Serial.parseFloat();
    // float y = Serial.parseFloat();

    // Clamp values to gravity
    // x = constrain(x, -gravity, gravity);
    // y = constrain(y, -gravity, gravity);  

    // Convert float → int for map()
    // int x_pwm = map(x, -gravity, gravity, 0, 255);
    // int y_pwm = map(y, -gravity, gravity, 0, 255);

    // analogWrite(ENABLE1, x_pwm);
    // analogWrite(ENABLE2, y_pwm);

    // LCD display
    // String inputString = Serial.readStringUntil('\n');
    // lcd.clear();

    // lcd.setCursor(0, 0);
    // lcd.print(inputString);
    // lcd.setCursor(1, 1);
    // lcd.print(y);
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\n' || inChar == '\r') {
      if (inputString.length() > 0) {
        stringComplete = true;
      }
    } else {
      inputString += inChar;
    }
  }
}
