#define LED_PIN 2 // FOR LED

#define SIGNAL_PIN 23    // sensor GPIO23 -> RaspberryPi
#define SENSOR_TX 16     // sensor TX -> this ESP32 RX pin
#define SENSOR_RX 17     // Unused

HardwareSerial mySerial(1); // use UART1

unsigned long signalTimeout = 0;
int lastDistance = -1;      // stores previous distance
unsigned long lastUpdate = 0;  
const unsigned long noMovementTimeout = 2000;  // 2 seconds of no change = no movement

void setup() {
  pinMode(LED_PIN, OUTPUT);  //FOR LED
  digitalWrite(LED_PIN, LOW); //FOR LED
  
  pinMode(SIGNAL_PIN, OUTPUT);
  digitalWrite(SIGNAL_PIN, LOW);

  Serial.begin(115200); // debug serial
  mySerial.begin(115200, SERIAL_8N1, SENSOR_TX, SENSOR_RX);

  Serial.println("Sensor test starting...");
}

void loop() {
  while (mySerial.available()) {

    String line = mySerial.readStringUntil('\n');
    line.trim();

    Serial.println("Sensor: " + line);

    // Only process lines that contain "Range"
    if (line.startsWith("Range")) {
      
      int dist = line.substring(6).toInt();  // extract distance number

      // First reading — initialize baseline
      if (lastDistance == -1) {
        lastDistance = dist;
        lastUpdate = millis();
      }

      // Check if distance changed
      if (abs(dist - lastDistance) > 30) {   // change threshold to ignore noise
        Serial.println("Movement detected!");

        digitalWrite(LED_PIN, HIGH); // FOR LED
        
        digitalWrite(SIGNAL_PIN, HIGH);        // Send HIGH to Pi
        signalTimeout = millis() + 1000; 
        
        lastDistance = dist;
        lastUpdate = millis();
      } else {
        // No movement detected, just update timestamp
        lastUpdate = millis();
      }
    }
  }

  // Reset the signal after timeout
  if (millis() > signalTimeout) {
    digitalWrite(LED_PIN, LOW);
    digitalWrite(SIGNAL_PIN, LOW);
  }

  delay(20);
}
