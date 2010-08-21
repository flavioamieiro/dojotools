#define PIN_RED 7
#define PIN_5_VOLTS 6
#define PIN_GREEN 5
#define PIN_BLUE 4
#define DELAY_TIME 1000

void setup(){
    Serial.begin(9600);
    pinMode(PIN_RED, OUTPUT);
    pinMode(PIN_5_VOLTS, OUTPUT);
    pinMode(PIN_GREEN, OUTPUT);
    pinMode(PIN_BLUE, OUTPUT);
    digitalWrite(PIN_BLUE, HIGH);
    digitalWrite(PIN_5_VOLTS, HIGH);
    digitalWrite(PIN_RED, HIGH);
    digitalWrite(PIN_GREEN, HIGH);
}

void turnPinOn(int pin){
    digitalWrite(PIN_RED, HIGH);
    digitalWrite(PIN_GREEN, HIGH);
    digitalWrite(PIN_BLUE, HIGH);
    digitalWrite(pin, LOW);
}

int pinIsOn(int pin){
  return digitalRead(pin) == LOW;
}

void turnOffAll(){
    digitalWrite(PIN_GREEN, HIGH);
    digitalWrite(PIN_RED, HIGH);
    digitalWrite(PIN_BLUE, HIGH);
}

void blinkPin(int pin){
    for (int i = 0; i < 3; i++){
        turnOffAll();
        delay(DELAY_TIME);
        turnPinOn(pin);
        delay(DELAY_TIME);
    }
}

void loop(){
    if (Serial.available()){
        char option = Serial.read();
        if (option == 'R'){
            if (pinIsOn(PIN_GREEN)){
                blinkPin(PIN_RED);
            } else {
                turnPinOn(PIN_RED);
            }
        }
        if (option == 'G'){
            if (pinIsOn(PIN_RED)){
                blinkPin(PIN_GREEN);
            } else {
                turnPinOn(PIN_GREEN);
            }
        }
    }
}
