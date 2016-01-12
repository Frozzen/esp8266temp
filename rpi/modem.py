# -*- coding: utf-8 -*-
from RPi import GPIO
from time import sleep
import sys, os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW) 	# modem PWR
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW) 	# modem PWR
GPIO.output(18, 1)
sleep(3) # пауза 3 секунды
GPIO.output(18, 0)
GPIO.output(17, 1) 		# включил модем
#sleep(1) # пауза 3 секунды
#GPIO.cleanup() # сброс всех выводо
