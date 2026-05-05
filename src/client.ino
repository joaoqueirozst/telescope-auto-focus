#include <WiFi.h>

const char* ssid = " - "; 
const char* password = " - ";
const char* host = " - ";
const int port = 1000;

const int PINpullup = 21; // opções PullUp: "5", 21, 22 e 23
const int PINMs = 16; //
const int PINDir = 15;
const int PINStep = 2;
const int steps_pv = 35200;
int meioperiodo = 1000;
int passos = 0;
int steps = 0;
int best = 0;
int info; //
String resposta;

void GiraMotor() {
  while (steps != passos) {
    if (steps > passos) {
      digitalWrite(PINDir, LOW);
      digitalWrite(PINStep, HIGH);
      delayMicroseconds(meioperiodo);
      digitalWrite(PINStep, LOW);
      delayMicroseconds(meioperiodo);
      passos++;
    }
    else if (steps < passos) {
      digitalWrite(PINDir, HIGH);
      digitalWrite(PINStep, HIGH);
      delayMicroseconds(meioperiodo);
      digitalWrite(PINStep, LOW);
      delayMicroseconds(meioperiodo);
      passos--;
    }
    delay(10);
  }
}

WiFiClient client;

void setup() {
  pinMode(PINpullup, INPUT_PULLUP); //
  pinMode(PINMs, OUTPUT);
  digitalWrite(PINMs, HIGH);
  pinMode(PINDir, OUTPUT);
  pinMode(PINStep, OUTPUT);

  info = digitalRead(PINpullup);
  while (info != 0) {
    steps++;
    GiraMotor();
    info = digitalRead(PINpullup);
    Serial.println("Iniciando...");
  }

  Serial.println("INDO POSICAO 0");
  steps = 0;
  passos = 3000;
  
  GiraMotor();
  if (passos == steps) {
    Serial.println("Lente em sua posicao inicial!");
  } //

  Serial.begin(115200);
  delay(10);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao Wi-Fi...");
  }
  Serial.println("Conectado ao Wi-Fi.");

  if (client.connect(host, port)) {
    Serial.println("\nConectado ao servidor Python.");
  }
  else {
    Serial.println("Falha na conexao ao servidor Python.");
  }
}

void loop() {
  if (client.available()) {
    resposta = client.readStringUntil('\r');
    Serial.println(resposta);

    steps = resposta.toInt();
    if ((steps >= 0) && (steps <= 3200)) {
      GiraMotor();
      Serial.println("Movimento concluido_<\n");
      client.println("ok");
    }
  }
}
