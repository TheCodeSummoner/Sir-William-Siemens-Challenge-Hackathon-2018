#include <Servo.h>

/* Initialise the string to handle incoming data */
String data = NULL;

/* Initialise index positions of data separators */
int firstCommaIndex = 0;
int secondCommaIndex = 0;
int thirdCommaIndex = 0;

/* Initialise values to store received data (each value is normalised to be between 0 and 255) */
int humidity = 0;
int temperature = 0;
int battery = 0;
int noise = 0;

/* Declare Servo objects */
Servo bladesMachine;

void setup() {
  /* Setup a serial connection to communicate with pi */
  Serial.begin(9600);

  /* Initialise pins to write data */
  pinMode(6, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(15, OUTPUT);

  /* Assign the servo to a pin */
  bladesMachine.attach(22);
}

void loop() {
  /* Check if there is data to be received */
  if (Serial.available()) {

    /* Parse the data to int */
    data = Serial.readString();

    /* Find separators */
    firstCommaIndex = data.indexOf(',');
    secondCommaIndex = data.indexOf(',', firstCommaIndex + 1);
    thirdCommaIndex = data.indexOf(',', secondCommaIndex + 1);

    /* Convert the values to int */
    humidity = data.substring(0, firstCommaIndex).toInt();
    temperature = data.substring(firstCommaIndex + 1, secondCommaIndex).toInt();
    battery = data.substring(secondCommaIndex + 1, thirdCommaIndex).toInt();
    noise = data.substring(thirdCommaIndex + 1).toInt();

    /* Handle next noise value */
    if (noise == 1) {
      digitalWrite(13, HIGH);
      delay(100);
      digitalWrite(14, HIGH);
      delay(100);
      digitalWrite(15, HIGH);
    }
    else {
      digitalWrite(13, LOW);
      delay(100);
      digitalWrite(14, LOW);
      delay(100);
      digitalWrite(15, LOW);
    }

    /* Handle DC motor */
    analogWrite(6, humidity);

    /* Handle the servo */
    bladesMachine.write(temperature);
  }
}
