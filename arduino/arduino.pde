#define pinRed 7
#define pin5Volts 6
#define pinGreen 5
#define pinBlue 4

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

void loop(){
  if (Serial.available()){
    char option = Serial.read();
    if (option == 'R'){
      turnRedOn();
    }
    if (option == 'G'){
      turnGreenOn();
    }
  }
}
