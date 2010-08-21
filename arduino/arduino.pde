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

void turnRedOn(){
    digitalWrite(pinRed, LOW);
    digitalWrite(pinGreen, HIGH);
    digitalWrite(pinBlue, HIGH);
}

void turnGreenOn(){
    digitalWrite(pinGreen, LOW);
    digitalWrite(pinRed, HIGH);
    digitalWrite(pinBlue, HIGH);
}

void turnOffAll(){
    digitalWrite(pinGreen, HIGH);
    digitalWrite(pinRed, HIGH);
    digitalWrite(pinBlue, HIGH);
}

void redIsOn(){
    return digitalRead(pinRed) == LOW;
}

void greenIsOn(){
    return digitalRead(pinGreen) == LOW
}

void blinkGreen(){
    for (int i = 0; i < 3; i++){
        turnOffAll();
        delay(delayTime);
        turnGreenOn();
        delay(delayTime);
    }
}

void blinkRed(){
    for (int i = 0; i < 3; i++){
        turnOffAll();
        delay(delayTime);
        turnRedOn();
        delay(delayTime);
    }
}

void loop(){
    if (Serial.available()){
        char option = Serial.read();
        if (option == 'R'){
            if (greenIsOn()){
                blinkRed();
            } else {
                turnRedOn();
            }
        }
        if (option == 'G'){
            if (redIsOn()){
                blinkGreen();
            } else {
                turnGreenOn();
            }
        }
    }
}
