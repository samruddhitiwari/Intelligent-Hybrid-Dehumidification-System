#include <DHT.h>

// ===== SENSOR SETUP =====
#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

// ===== PINS =====
int pwm1 = 5;      // XY-MOS 1 (Peltier 1)
int pwm2 = 6;      // XY-MOS 2 (Peltier 2)
int relayPin = 8;  // Relay (Pump)

// ===== SETUP =====
void setup() {

  Serial.begin(9600);
  dht.begin();

  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(relayPin, OUTPUT);

  // Pump OFF initially (active LOW relay)
  digitalWrite(relayPin, HIGH);
}

// ===== LOOP =====
void loop() {

  // === READ SENSOR ===
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Send only valid readings
  if (!isnan(h) && !isnan(t)) {

    Serial.print(h);
    Serial.print(",");
    Serial.println(t);
  }

  delay(200);

  // === RECEIVE ML OUTPUT ===
  if (Serial.available()) {

    int level = Serial.parseInt();   // 0,1,2

    int pwmVal1 = 0;
    int pwmVal2 = 0;

    // ===== CONTROL LOGIC =====

    // LEVEL 0 → LOW HUMIDITY
    if (level == 0) {

      pwmVal1 = 0;
      pwmVal2 = 0;

      // Pump ON
      digitalWrite(relayPin, LOW);
    }

    // LEVEL 1 → MEDIUM HUMIDITY
    else if (level == 1) {

      pwmVal1 = 150;
      pwmVal2 = 0;

      // Pump ON
      digitalWrite(relayPin, LOW);
    }

    // LEVEL 2 → HIGH HUMIDITY
    else if (level == 2) {

      pwmVal1 = 255;
      pwmVal2 = 255;

      // Pump OFF
      digitalWrite(relayPin, HIGH);
    }

    // APPLY PWM
    analogWrite(pwm1, pwmVal1);
    analogWrite(pwm2, pwmVal2);
  }

  delay(800);
}
