#include <LiquidCrystal.h>

// Initialize library with the interface pins
const int rs = 7, en = 8, d4 = 9, d5 = 10, d6 = 11, d7 = 12;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

char CLEAR_KEY = '`';

// define the pins for a single motor
#define ENABLE 5
#define DIRA 6 // was pin 3 in the elegoo tutorial
#define DIRB 4



void setup() {
  //---set pin direction
  pinMode(ENABLE,OUTPUT);
  pinMode(DIRA,OUTPUT);
  pinMode(DIRB, OUTPUT);

  // Set a default direction (forward)
  digitalWrite(DIRA, HIGH);
  digitalWrite(DIRB, LOW);

  lcd.begin(16, 2);           // Set up 16 columns and 2 rows
  Serial.begin(9600);         // Start serial communication at 9600 bps

  lcd.print("Input:");
  lcd.setCursor(0, 1);
}

void loop() {
  // Check if data is available from the keyboard (Serial Monitor)
  if (Serial.available()) {
    char input = Serial.read(); // Read the character
    
    if (input == CLEAR_KEY) {
      lcd.clear();
    } else {
      if (input >= '0' && input <= '9') { // Check if the character is between '0' and '9'
        int integer_input = input - '0'; // Convert ASCII character to its actual numeric value
        int mapped_integer_input = map(integer_input, 0, 9, 0, 255);
      lcd.print(mapped_integer_input); // Display the command on LCD
      lcd.setCursor(0,1);
      analogWrite(ENABLE, mapped_integer_input);
      };
    };
  };
};