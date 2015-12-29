# esp8266temp
отправление температуры с нескольких термометров на thingspeak.com

- измеритель температуры на esp8266, ds1802
- OLED дисплей SSD1306 прокручивает температуру на экране
- конфигуратор из WiFiSafe mode - сервер позволяющий задать:
    - параметры WiFi 
    - названия термометров, флаг какие показывать на экране
    - ключ thingspeak.com
    - период обновления
- отправлять данные на thingspeak.com через WiFi router
- измерять температуру в N точках

Пишется на arduino IDE с библиотеками:

http://esp8266.ru/arduino-ide-esp8266/ - IDE
https://github.com/milesburton/Arduino-Temperature-Control-Library
https://github.com/Links2004/arduinoWebSockets
https://github.com/somhi/ESP_SSD1306


https://www.raspberrypi.org/forums/viewtopic.php?t=27379&p=505250 - 1 wire RPi
https://gist.github.com/kmpm/4445289
https://www.carluccio.de/1-wire-sensoren-am-raspberry-pi/
sudo apt-get install i2c-tools owfs ow-shell

