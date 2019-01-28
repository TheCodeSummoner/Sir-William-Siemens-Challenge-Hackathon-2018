#include <FastLED.h>
#define NUM_LEDS 60
#define DATA_PIN 6

/* Initialise the string to handle incoming data */
String data = NULL;

/* Initialise index positions of data separators */
int firstCommaIndex = 0;
int secondCommaIndex = 0;

/* Initialise values to store received data (each value is normalised to be between 0 and 255) */
int red_led = 0;
int green_led = 0;
int blue_led = 0;

/* Declare an array to store the information about ids */
CRGB leds[NUM_LEDS];

void setup() {
  /* Setup a serial connection to communicate with pi */
  Serial.begin(9600);

  /* Initialise LEDs */
  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);

  /* Initialise pins to write data */
  pinMode(6, OUTPUT);
}

void loop() {
  /* Check if there is data to be received */
  if (Serial.available()) {

    /* Parse the data to int */
    data = Serial.readString();

    /* Find separators */
    firstCommaIndex = data.indexOf(',');
    secondCommaIndex = data.indexOf(',', firstCommaIndex + 1);

    /* Convert the values to int */
    red_led = data.substring(0, firstCommaIndex).toInt();
    green_led = data.substring(firstCommaIndex + 1, secondCommaIndex).toInt();
    blue_led = data.substring(secondCommaIndex + 1).toInt();

    /* Flash next sequence of LEDs */
    for(int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CRGB(green_led, red_led, blue_led);
      FastLED.show();
    }
  }
}
