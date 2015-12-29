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
    
https://www.raspberrypi.org/forums/viewtopic.php?t=27379&p=505250 - 1 wire RPi
https://gist.github.com/kmpm/4445289
https://www.carluccio.de/1-wire-sensoren-am-raspberry-pi/

FAQ Register Login￼
Search…
 ￼
Linux kernel is now 3.18

Post a reply   69 posts   Page 2 of 3   123
by ame » Wed Jan 21, 2015 1:10 am
Here's the detective work I have managed so far. In /var/log/dmesg I have this:
CODE: SELECT ALL
[    6.020730] Driver for 1-wire Dallas network protocol.
[    6.134665] w1-gpio onewire@0: gpio pin 4, gpio pullup pin 1
[    6.230123] w1_add_master_device: set_pullup requires write_byte or touch_bit, disabling


I don't know why the pullup is on pin 1. My one-wire bus is hooked up to pin 4.

[Edit: This might be a red herring. It's all working when I stopped device tree from loading.]
Last edited by ame on Wed Jan 21, 2015 7:30 am, edited 1 time in total.
Posts: 3174
Joined: Sat Aug 18, 2012 1:21 am
Location: Korea
by Sheddyian » Wed Jan 21, 2015 1:56 am
I wasn't familiar with using rpi-update to select different versions of firmware, so this took me a while, but I can now confirm that
reverting to the previous firmware with :
CODE: SELECT ALL
sudo rpi-update f74b92120e0d469fc5c2dc85b2b5718d877e1cbb


fixes the problem, and I can now measure the temperature with the 1 wire probe. It's currently 2.56C outside where I am ￼

Ian

