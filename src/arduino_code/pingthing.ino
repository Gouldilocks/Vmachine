
#include "NewPing.h"

// Setup The pins and maximum Ping distance.
int TRIGGER_PIN = 28;
int ECHO_PIN = 26;
int MAX_PING_DISTANCE = 200; // centimeters

// Declare NewPing object
NewPing pingSensor(TRIGGER_PIN, ECHO_PIN, MAX_PING_DISTANCE);

void setup() {
  Serial.begin(9600);
}

void loop() {
//    Serial.println(pingSensor.ping_cm());
    if(Serial.available() > 0){
      String data = Serial.readStringUntil('\n');
    // print the data for the ping sensor to the serial monitor

//    Serial.println(10);    
    Serial.println(pingSensor.ping_cm());
    }
}
  
