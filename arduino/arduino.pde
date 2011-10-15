#define PIN_RED 7
#define PIN_GREEN 8
#define DELAY_TIME 700

void setup(){
    Serial.begin(9600);
    pinMode(PIN_RED, OUTPUT);
    pinMode(PIN_GREEN, OUTPUT);
    digitalWrite(PIN_RED, HIGH);
    digitalWrite(PIN_GREEN, LOW);
}

void turnOffAll(){
    digitalWrite(PIN_GREEN, LOW);
    digitalWrite(PIN_RED, LOW);
}
 
void blinkPin(int pin){
    for (int i = 0; i < 3; i++){
        turnOffAll();
        delay(DELAY_TIME);
        digitalWrite(pin, HIGH);
        delay(DELAY_TIME);
    }
}

void blinkAll(){
    for (int i = 0; i < 3; i++){
        turnOffAll();
        delay(DELAY_TIME);
        digitalWrite(PIN_RED, HIGH);
        digitalWrite(PIN_GREEN, HIGH);
        delay(DELAY_TIME);
        turnOffAll();
    }
}

boolean pinIsOn(int pin){
    return digitalRead(pin) == HIGH;
} 
  
void loop(){
    if (Serial.available()){
        char option = Serial.read();
        if (option == 'R'){
            if (pinIsOn(PIN_GREEN)){
                digitalWrite(PIN_GREEN, LOW);
                blinkPin(PIN_RED);
            } else {
                digitalWrite(PIN_RED, HIGH);
            }
        }
        if (option == 'G'){
            if (pinIsOn(PIN_RED)){
                digitalWrite(PIN_RED, LOW);
                blinkPin(PIN_GREEN);
            } else {
                digitalWrite(PIN_GREEN, HIGH);
            }
        }
        if (option == 'T'){
            int currentPin = 0;
            if (pinIsOn(PIN_GREEN)){
              currentPin = PIN_GREEN;
            } else if (pinIsOn(PIN_RED)){
              currentPin = PIN_RED;
            }
            blinkAll();
            digitalWrite(currentPin, HIGH);
        }
    }
}
