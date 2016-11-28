#include <ESP8266WiFi.h>

// WiFi parameters to be configured
const char* ssid = "crunchytown";
const char* password = "zxasqw12";

#define LED_PIN 2

void setup(void)
{
  delay(1000);
  Serial.begin(9600);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  
  // while wifi not connected yet, print '.'
  // then after it connected, get out of the loop
  while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
  }
  //print a new line, then print WiFi connected and the IP address
  Serial.println("");
  Serial.println("WiFi connected");  
  
  // Print the IP address
  Serial.println(WiFi.localIP());

  pinMode(LED_PIN, OUTPUT);
}

void loop(void)
{
  if (WiFi.status() == WL_CONNECTED){
    digitalWrite(LED_PIN, HIGH);
  }
  else {
    digitalWrite(LED_PIN, LOW);
  }
}




