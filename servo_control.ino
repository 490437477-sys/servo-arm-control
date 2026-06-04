#include <Servo.h>

// Joystick pins
const int joy1XPin = A0, joy1YPin = A1, joy1Btn = 2;
const int joy2XPin = A3, joy2YPin = A2, joy2Btn = 4;
const int ledPin = 3;

// Servo pins
const int servoPins[] = {5, 9, 10, 11, 7};
Servo servos[5];
int angles[] = {90, 90, 90, 90, 90};
int targets[] = {90, 90, 90, 90, 90};

// Dead zone
const int deadZone = 50;
unsigned long lastBtn1 = 0, lastBtn2 = 0;
const int debounce = 50;
const int moveDelay = 50;
unsigned long lastMove = 0;

void setup() {
  pinMode(joy1Btn, INPUT_PULLUP);
  pinMode(joy2Btn, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  for (int i = 0; i < 5; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(angles[i]);
    delay(80);
  }
  digitalWrite(ledPin, HIGH);
  
  Serial.begin(9600);
  while (!Serial) delay(10);
  
  printHelp();
}

void loop() {
  unsigned long now = millis();
  
  if (now - lastMove < moveDelay) {
    delay(moveDelay - (now - lastMove));
    return;
  }
  lastMove = now;

  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    if (input.length() > 0) {
      Serial.print("> "); Serial.println(input);
      processCommand(input);
    }
  }

  for (int i = 0; i < 5; i++) {
    if (angles[i] < targets[i]) angles[i]++;
    else if (angles[i] > targets[i]) angles[i]--;
    servos[i].write(angles[i]);
  }

  int j1x = analogRead(joy1XPin) - 512;
  int j1y = analogRead(joy1YPin) - 512;
  int j2x = analogRead(joy2XPin) - 512;
  int j2y = analogRead(joy2YPin) - 512;

  if (j1x < -deadZone) { targets[0] = max(0, targets[0] - 1); angles[0] = targets[0]; }
  if (j1x > deadZone) { targets[0] = min(180, targets[0] + 1); angles[0] = targets[0]; }
  if (j1y < -deadZone) { targets[1] = max(0, targets[1] - 1); angles[1] = targets[1]; }
  if (j1y > deadZone) { targets[1] = min(180, targets[1] + 1); angles[1] = targets[1]; }
  if (j2x < -deadZone) { targets[2] = max(0, targets[2] - 1); angles[2] = targets[2]; }
  if (j2x > deadZone) { targets[2] = min(180, targets[2] + 1); angles[2] = targets[2]; }
  if (j2y < -deadZone) { targets[3] = max(0, targets[3] - 1); angles[3] = targets[3]; }
  if (j2y > deadZone) { targets[3] = min(180, targets[3] + 1); angles[3] = targets[3]; }

  if (digitalRead(joy1Btn) == LOW && now - lastBtn1 > debounce) {
    targets[4] = min(90, targets[4] + 2);
    angles[4] = targets[4];
    lastBtn1 = now;
  }
  if (digitalRead(joy2Btn) == LOW && now - lastBtn2 > debounce) {
    targets[4] = max(0, targets[4] - 2);
    angles[4] = targets[4];
    lastBtn2 = now;
  }
}

void printHelp() {
  Serial.println("=== Servo Control ===");
  Serial.println("0 90  : Servo0=90");
  Serial.println("1 45  : Servo1=45");
  Serial.println("2 180 : Servo2=180");
  Serial.println("3 90  : Servo3=90");
  Serial.println("4 60  : Servo4=60");
  Serial.println("90    : ALL=90");
  Serial.println("90 90 90 90 90 : Batch");
  Serial.println("==========");
}

void processCommand(String cmd) {
  cmd.trim();
  cmd.toLowerCase();
  
  int count = 0;
  int vals[5] = {90, 90, 90, 90, 90};
  int start = 0;
  
  for (int i = 0; i <= cmd.length() && count < 5; i++) {
    if (cmd.charAt(i) == ' ' || i == cmd.length()) {
      String num = cmd.substring(start, i);
      vals[count++] = num.toInt();
      start = i + 1;
    }
  }
  
  if (count == 5) {
    for (int i = 0; i < 5; i++) {
      if (vals[i] >= 0 && vals[i] <= 180) {
        targets[i] = vals[i];
      }
    }
    Serial.print("OK:"); 
    for (int i = 0; i < 5; i++) { Serial.print(targets[i]); if (i < 4) Serial.print(","); }
    Serial.println();
    return;
  }
  
  if (count == 1 && vals[0] >= 0 && vals[0] <= 180) {
    for (int i = 0; i < 5; i++) targets[i] = vals[0];
    Serial.print("ALL:"); Serial.println(vals[0]);
    return;
  }
  
  if (count == 2) {
    int servoNum = vals[0];
    int angleVal = vals[1];
    if (servoNum >= 0 && servoNum <= 4 && angleVal >= 0 && angleVal <= 180) {
      targets[servoNum] = angleVal;
      Serial.print("S"); Serial.print(servoNum); Serial.print(":"); Serial.println(angleVal);
      return;
    }
  }
  
  Serial.println("?");
}
