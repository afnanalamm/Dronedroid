#include <LiquidCrystal.h>

// Initialize library with the interface pins
const int rs = 7, en = 8, d4 = 9, d5 = 10, d6 = 11, d7 = 12;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

#define ENABLE1 5
#define ENABLE2 3
#define DIR1 6
#define DIR2 4

const float gravity = 1;

void setup() {
  pinMode(ENABLE1, OUTPUT);
  pinMode(ENABLE2, OUTPUT);
  pinMode(DIR1, OUTPUT);
  pinMode(DIR2, OUTPUT);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, HIGH);

  lcd.begin(16, 2);
  Serial.begin(9600);

  lcd.print("X,Y Input:");
  lcd.setCursor(0, 1);
}

void loop() {
  if (Serial.available()) {

    // Read X and Y as floats: "x,y\n"
    float x = Serial.parseFloat();
    float y = Serial.parseFloat();

    // Clamp values to gravity
    x = constrain(x, -gravity, gravity);
    y = constrain(y, -gravity, gravity);

    // Convert float → int for map()
    int x_pwm = map(x * 100, -gravity * 100, gravity * 100, 0, 255);
    int y_pwm = map(y * 100, -gravity * 100, gravity * 100, 0, 255);

    analogWrite(ENABLE1, x_pwm);
    analogWrite(ENABLE2, y_pwm);

    // LCD display

    lcd.setCursor(0, 1);
    lcd.print(x_pwm);
    lcd.setCursor(1, 1);
    lcd.print(y_pwm);
  }
}
