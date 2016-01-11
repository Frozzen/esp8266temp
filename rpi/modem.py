# -*- coding: utf-8 -*-
from RPi import GPIO
from time import sleep
import sys, os

print "Use modem.py power restart"
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) 	# modem PWR
GPIO.setup(18, GPIO.OUT) 	# modem RST
GPIO.output(17, False)
GPIO.output(18, False)
sleep(1) # пауза 3 секунды
GPIO.output(17, True) 		# включил модем

GPIO.cleanup() # сброс всех выводо
