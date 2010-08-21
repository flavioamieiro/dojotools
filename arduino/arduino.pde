#define pinRed 7
#define pin5Volts 6
#define pinGreen 5
#define pinBlue 4
#define delayTime 1000

void setup(){
    Serial.begin(9600);
    pinMode(pinRed, OUTPUT);
    pinMode(pin5Volts, OUTPUT);
    pinMode(pinGreen, OUTPUT);
    pinMode(pinBlue, OUTPUT);
    digitalWrite(pinBlue, HIGH);
    digitalWrite(pin5Volts, HIGH);
    digitalWrite(pinRed, HIGH);
    digitalWrite(pinGreen, HIGH);
}

void turnPinOn(int pin){
    digitalWrite(pinRed, HIGH);
    digitalWrite(pinGreen, HIGH);
    digitalWrite(pinBlue, HIGH);
    digitalWrite(pin, LOW);
}

int pinIsOn(int pin){
  return digitalRead(pin) == LOW;
}

void turnOffAll(){
    digitalWrite(pinGreen, HIGH);
    digitalWrite(pinRed, HIGH);
    digitalWrite(pinBlue, HIGH);
}

void blinkPin(int pin){
    for (int i = 0; i < 3; i++){
        turnOffAll();
        delay(delayTime);
        turnPinOn(pin);
        delay(delayTime);
    }
}

void loop(){
    if (Serial.available()){
        char option = Serial.read();
        if (option == 'R'){
            if (pinIsOn(pinGreen)){
                blinkPin(pinRed);
            } else {
                turnPinOn(pinRed);
            }
        }
        if (option == 'G'){
            if (pinIsOn(pinRed)){
                blinkPin(pinGreen);
            } else {
                turnPinOn(pinGreen);
            }
        }
    }
}
