
String text = "";

// int LED_BUILTIN = 6;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(9600);
  delay(50);
  
  pinMode(LED_BUILTIN, OUTPUT);
}
// the loop function runs over and over again forever
void loop() {
  text = "";
  // Serial.println(text);
  
  // serial read section
  while (Serial.available()) { // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
    delay(30);  //delay to allow buffer to fill 
    if (Serial.available() > 0) {
      char c = Serial.read();  //gets one byte from serial buffer
      text += c; //makes the string text
    }
}
   if (text[0] == 't') {
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
}
