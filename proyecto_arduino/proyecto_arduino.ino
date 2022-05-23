int leds[4] = { 2, 3, 4, 5};

void setup() {

  for (int i = 0; i < 4; i++)
  {
    pinMode(leds[i], OUTPUT);
  }
  pinMode(7, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);

  Serial.begin(9600);

}
int v[5] = {0, 0, 0, 0, 0};
int vpulsador, vpulsador2;
String cadena = "";
void loop() {

  v[0] = map(analogRead(A0), 0, 1023, 1, 5);
  v[1] = map(analogRead(A1), 0, 1023, 1, 5);
  v[2] = map(analogRead(A2), 0, 1023, 1, 5);
  v[3] = map(analogRead(A3), 0, 1023, 1, 5);
  v[4] = map(analogRead(A4), 0, 1023, 1, 5);

  vpulsador = digitalRead(7);
  vpulsador = digitalRead(6);
  cadena = "I";
  for (int i = 0; i < 5; i++)
  {
    cadena += String(v[i]) + ";";
  }
  cadena += String(!vpulsador) + ";" + String(!vpulsador2) + "T";
  Serial.println(cadena);
  if (Serial.available() > 0) {
    int valor = Serial.readString().toInt();
    digitalWrite(leds[valor], 1);
    delay(2000);
    digitalWrite(leds[valor], 0);
    delay(500);
  }
  delay(500);

}
