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

Пока запускаем на RPI
    - простой по реализации вариант
    /etc/rc.local
	modprobe w1-gpio
	modprobe w1-therm

https://www.carluccio.de/1-wire-sensoren-am-raspberry-pi/

Откатил на ядро 3.12.36+ и все заработало

sudo rpi-update f74b92120e0d469fc5c2dc85b2b5718d877e1cbb


fixes the problem, and I can now measure the temperature with the 1 wire probe. It's currently 2.56C outside where I am ￼

Ian

