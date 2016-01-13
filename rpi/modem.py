# -*- coding: utf-8 -*-
"""
включить кодем через GPIO

ключи
    --on - принудительно включить/выключить
    --test проверит что модем работает
    --check проверить и включить если не работает
"""
from RPi import GPIO
from time import sleep
import sys, os
import serial
import getopt


def do_reset(ser):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)  # modem PWR
    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)  # modem PWR
    GPIO.output(18, 1)
    sleep(3)
    GPIO.output(18, 0)
    GPIO.output(17, 1)  # включил модем
    sleep(1)
    # GPIO.cleanup() # сброс всех выводов


def do_test_modem(ser):
    """
    проверить что модем отвечает и в нормальном состоянии,
    показывать соту где зарегистрирован

    AT +CREG:  Network Registration

    :type ser: serial.serialposix.Serial
    :return:  None что то не так
        состояние на нормальное строка регистрации,
        +CREG: <mode>,<stat>,<lac>,<ci>
            <stat>:	decimal (0-5); Status
              0  	not registered
              1  	registered (home)
              2  	not registered (searching)
              3  	registration denied
              4  	unknown
              5  	registered (roaming)
        +CREG: 2,1,"9844","12F5"
    """
    # режим показывать соту где зарегистрирован
    ser.write("at+creg=2\r")
    d = ser.read(100)
    try:
        d.index('OK') 

        ser.write("at+creg?\r")
	d = ser.read(100)
        d.index('OK')
    except ValueError:
	return None
    s = d.split('\r')[2][1:]
    return s


def wait_signal(ser, timeout=600):
    """
    дожидаемся появления регистрации

    :param timeout: ждем не более указанного кол-ва секунд
    :param ser:
    :return: (False, infoStr) модем в неправильном режиме,
        (True, infoStr) - есть регистрация
    """
    while timeout > 0:
        r = do_test_modem(ser)
        if r is None:
            return False, 'modem is in wrong state'
        if r.split(',')[1] == '1':
            return True, r
        sleep(1)
    return False, 'no network'


def usage():
    print(__doc__)
    sys.exit(1)


def do_check(ser):
    while 1:
        r, msg = wait_signal(ser)
        if r == False:
            print msg
	    sleep(10)
            do_reset(ser)
        else:
            return msg


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'toc', ['test', 'on', 'check'])
    except getopt.GetoptError as error:
        print error
        usage()
    ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=1)
    for o, a in opts:
        if o in ('-t', '--test'):
            print "test:", do_test_modem(ser)
        elif o in ('-o', '--on'):
            do_reset(ser)
        elif o in ('-c', '--check'):
            print do_check(ser)
        else:
            usage()
