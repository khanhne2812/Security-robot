#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>
#include "DHT.h"

// Firebase configuration
#define FIREBASE_HOST "************"
#define FIREBASE_AUTH "************"

// WiFi configuration
#define WIFI_SSID "******"
#define WIFI_PASSWORD "******"

// DHT sensor configuration
#define DHTPIN 5
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// MQ2 sensor configuration
int smokeA0 = A0;
String path = "/";

// Firebase objects
FirebaseData firebaseData;
FirebaseConfig firebaseConfig;
FirebaseAuth firebaseAuth;

void initFirebase() {

    
    //Firebase.begin(&firebaseConfig, &firebaseAuth);
    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
    Firebase.reconnectWiFi(true);
    if (!Firebase.beginStream(firebaseData, path)) {
        Serial.println("Failed to begin stream to Firebase.");
        Serial.println("REASON: " + firebaseData.errorReason());
        Serial.println();
    }
    else{
    Serial.println("Firebase connection successful.");
    }
}

void setup() {
    Serial.begin(115200);
    dht.begin();
    pinMode(smokeA0, INPUT);

    // Connect to WiFi
    Serial.print("Connecting to ");
    Serial.print(WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    Serial.println();
    Serial.print("Connected. IP Address: ");
    Serial.println(WiFi.localIP());


    initFirebase();

}


void loop() {
    int analogSensor = analogRead(smokeA0);
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
        Serial.println("Failed to read from DHT sensor!");
    }

    Serial.print("Temperature: ");
    Serial.print(t);
    Serial.print(" °C, Humidity: ");
    Serial.print(h);
    Serial.print(" %, MQ2: ");
    Serial.println(analogSensor);

    if (!Firebase.setFloat(firebaseData, "/Temp", t)) {
        Serial.print("Failed to send Temperature to Firebase: ");
        Serial.println(firebaseData.errorReason());
    }
    if (!Firebase.setFloat(firebaseData, "/Humidity", h)) {
        Serial.print("Failed to send Humidity to Firebase: ");
        Serial.println(firebaseData.errorReason());
    }
    if (!Firebase.setFloat(firebaseData, "/MQ2", analogSensor)) {
        Serial.print("Failed to send MQ2 sensor value to Firebase: ");
        Serial.println(firebaseData.errorReason());
    }

    delay(5000);  // Delay between readings
}
