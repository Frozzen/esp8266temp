# esp8266temp
отправление температуры с нескольких термометров на thingspeak.com

## измеритель температуры на esp8266, ds1820 

### версия 1
- отправлять данные на thingspeak.com через WiFi router
- измерять температуру в N точках

### версия 2  
- OLED дисплей SSD1306 прокручивает температуру на экране

### версия 3 
- конфигуратор из WiFiSafe mode - сервер позволяющий задать:
    - параметры WiFi 
    - названия термометров, флаг какие показывать на экране
    - ключ thingspeak.com
    - период обновления

Пишется на arduino IDE с библиотеками:

http://esp8266.ru/arduino-ide-esp8266/ - IDE
https://github.com/milesburton/Arduino-Temperature-Control-Library
https://github.com/Links2004/arduinoWebSockets
https://github.com/somhi/ESP_SSD1306
https://learn.sparkfun.com/tutorials/esp8266-thing-hookup-guide/example-sketch-ap-web-server

# Пока запускаем на RPI

Пока запускаем простой по реализации вариант
/etc/rc.local:

	modprobe w1-gpio
	modprobe w1-therm

https://www.carluccio.de/1-wire-sensoren-am-raspberry-pi/

4.х ядро парит. Откатил на ядро 3.12.36+ и все заработало

    sudo rpi-update f74b92120e0d469fc5c2dc85b2b5718d877e1cbb
    
http://wiki.iteadstudio.com/RPI_SIM900_GSM/GPRS_ADD-ON_V1.0 

## использование

посмотреть список устройств

    python things.py --list

послать данные по ключу

    python things.py --send=APIKEY

    
