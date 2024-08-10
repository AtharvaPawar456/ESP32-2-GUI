#include <Arduino.h>

const int ledPin = LED_BUILTIN;  // Use the built-in LED pin

void setup() {
  // Start serial communication at baud rate 115000
  Serial.begin(9600);
  
  // Seed random number generator
  randomSeed(analogRead(0));
  
  // Initialize the LED pin as an output
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Generate random values for each sensor
  int eventId = random(100, 200);  // Event ID: Random between 100 and 200
  float spo2 = random(950, 1000) / 10.0;  // Spo2: Random between 95.0 and 100.0
  int heartRate = random(60, 100);  // Heart Rate: Random between 60 and 100
  float pressureValue = random(1100, 1300) / 10.0;  // Pressure Value: Random between 110.0 and 130.0
  float temperatureValue = random(360, 380) / 10.0;  // Temperature Value: Random between 36.0 and 38.0
  int audioDataValue = random(50, 100);  // Audio Data Value: Random between 50 and 100
  float xPositionValue = random(-100, 100) / 10.0;  // X Position Value: Random between -10.0 and 10.0
  float yPositionValue = random(-100, 100) / 10.0;  // Y Position Value: Random between -10.0 and 10.0
  float zPositionValue = random(-100, 100) / 10.0;  // Z Position Value: Random between -10.0 and 10.0

  // Create the formatted string
  String dataString = String("Eventid: ") + eventId +
                      ", Spo2: " + spo2 +
                      ", Heart: " + heartRate +
                      ", Pres: " + pressureValue +
                      ", Temp: " + temperatureValue +
                      ", Audio: " + audioDataValue +
                      ", Xval: " + xPositionValue +
                      ", Yval: " + yPositionValue +
                      ", Zval: " + zPositionValue;

  // Send the formatted string to the serial monitor
  Serial.println(dataString);

  // Blink the LED
  digitalWrite(ledPin, HIGH);  // Turn the LED on
  delay(100);                  // Wait for 100 milliseconds
  digitalWrite(ledPin, LOW);   // Turn the LED off
  delay(100);                  // Wait for 100 milliseconds

  // Wait for 1 second before generating new values
  delay(1000);
}
