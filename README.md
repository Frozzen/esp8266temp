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
    
## настройка связи

    11	GPIO0	SIM900-PWERKEY	Powering-on key via software
    12	GPIO1	SIM900-RST	Resetting key via software
    
    >>> import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    >>> GPIO.setup(18, GPIO.OUT)
    >>> GPIO.output(18, False)

ни один вариант пока не пошел! WiFi не надежен - может вырубиться, потом его надо включать руками, USB сбои.

http://wiki.iteadstudio.com/RPI_SIM900_GSM/GPRS_ADD-ON_V1.0 

http://trustoff.ru/razblokirovka-routerov-huawei-e5830-e5832-e5832S-e585-e5838-besplatno

http://4pda.ru/forum/index.php?showtopic=254811&st=0#entry8361673

    https://www.thefanclub.co.za/how-to/how-setup-usb-3g-modem-raspberry-pi-using-usbmodeswitch-and-wvdial
    
    
    http://pastebin.com/EnurgyAC
   sudo apt-get install ppp usb-modeswitch wvdial

   pi@raspberrypi ~ $ lsusb
    Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. 
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. 
    Bus 001 Device 005: ID 12d1:142d Huawei Technologies Co., Ltd. 
    
  /etc/usb_modeswitch.conf
    DefaultVendor=  0x12d1
    DefaultProduct= 0x142d
    TargetVendor=   0x12d1
    TargetProduct=  0x1401
    TargetClass=    not set
    TargetProductList=""
    
    DetachStorageOnly=0
    HuaweiMode=0
    SierraMode=0
    SonyMode=0
    GCTMode=0
    KobilMode=0
    MessageEndpoint=  not set
    MessageContent="55534243123456780000000000000011062000000100000000000000000000"
    NeedResponse=0
    ResponseEndpoint= not set
    Interface=0x00
    
  run  
    sudo usb_modeswitch -I -W -c /etc/usb_modeswitch.d/12d1\:142d
    sudo usb_modeswitch -v 0x12d1 -p 0x142d -V 0x12d1 -P 0x1401 -c /etc/usb_modeswitch.conf  
    
  sudo leafpad /etc/wvdial.conf

  Replace the content of the file with the following. 

    [Dialer 3gconnect]
    Init1 = ATZ
    Init2 = ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0
    Init3 = AT+CGDCONT=1,"IP","internet.mts.ru"
    Stupid Mode = 1
    Modem Type = Analog Modem
    ISDN = 0
    Phone = *99#
    Modem = /dev/gsmmodem
    Username = mts
    Password = mts
    Baud = 460800
    
  sudo usb_modeswitch -c /etc/usb_modeswitch.conf
  wvdial 3gconnect
  не заработало
    
/etc/network/interfaces - старый    
    allow-hotplug wlan0
    auto wlan0
    iface wlan0 inet static
        wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
        address 192.168.1.6
        netmask 255.255.255.0
        gateway 192.168.1.1

 sudo apt-get install wicd-curses
## использование

посмотреть список устройств

    python things.py --list

послать данные по ключу

    python things.py --send=APIKEY

    
