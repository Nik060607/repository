// Библиотека Arduino.h подключается автоматически
#include <Arduino.h>

// Назначаем номер контакта, к которому подключён встроенный светодиод
const int ledPin = LED_BUILTIN; // Обычно контакт D13 для Arduino Nano

// Переменная состояния светодиода
bool ledState = LOW;

// Интервал переключения светодиода (в миллисекундах)
unsigned long previousMillis = 0;
const unsigned long interval = 1000; // интервал в 1 секунду

void setup() {
  // Устанавливаем режим вывода для контакта светодиода
  pinMode(ledPin, OUTPUT);

  // Запуск последовательного порта для вывода сообщений
  Serial.begin(9600); // Открываем последовательный порт
  delay(1000);        // Ждем, пока откроется COM-порт
  Serial.println("Программа запущена!");
}

void loop() {
  // Получаем текущее значение времени в миллисекундах
  unsigned long currentMillis = millis();

  // Проверяем, прошло ли нужное количество времени с последнего изменения состояния светодиода
  if ((currentMillis - previousMillis >= interval)) {
    // Обновляем предыдущее время
    previousMillis = currentMillis;
    
    // Меняем состояние светодиода
    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }
    
    // Выводим сообщение в монитор порта
    Serial.print("LED ");
    Serial.print((ledState == HIGH ? "включен." : "выключен."));
    Serial.print("\\n");
    
    // Включаем или выключаем светодиод
    digitalWrite(ledPin, ledState);
  }
}