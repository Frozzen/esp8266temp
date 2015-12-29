#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    получаем температуру c DS1802 и отправляем ее на thingspeak.com
    RPI:
    usage:
        python things.py --send померить и отослать температуру
        python things.py --list показать список термометров

    пример кода
    http://stackoverflow.com/questions/30889872/how-to-post-api-in-thingspeak-comusing-urllib-in-python
    https://electrosome.com/ds18b20-sensor-raspberry-pi-python/
"""
import urllib
import httplib
import glob
import time
import getopt, sys


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()  # read the device details
    f.close()
    return lines


def read_temp(dev):
    """
    прочитать температуру и конвертировать
    :param dev:
    :return:
    """
    lines = read_temp_raw(dev)
    while lines[0].strip()[-3:] != 'YES':  # ignore first line
        time.sleep(0.2)
        lines = read_temp_raw(dev)
    equals_pos = lines[1].find('t=')  # find temperature in the details
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0  # convert to Celsius
        return temp_c


def readAll(device_folders):
    """
    прочитать все датчики

    :rtype : dict {dev_file: value}
    :param device_folders:
    :return:
    """
    res = {}
    for device_folder in device_folders:
        device_file = device_folder + '/w1_slave'  # store the details
        res[device_folder] = read_temp_raw(device_file)
    return res


def sendTemp(val):
    # chanId: 74111; field[1-4]:room1temp, hotWaterTemp, coldWaterTemp, tempOutside
    # http://184.106.153.149
    params = urllib.urlencode({'key': 'IL6Q4TBCJGSA9CVF',
                               'field1': '19',
                               'field2': '43',
                               'field3': '23',
                               'field4': '-3'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
    except Exception as e:
        print "connection failed", e


def main():
    base_dir = '/sys/bus/w1/devices/'  # point to the address
    device_folder = glob.glob(base_dir + '28*')  # find devices with address starting from 28*

    res = readAll(device_folder)
    sendTemp(res)


def usage():
    print __doc__
    sys.exit(1)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'sl', ['send', 'list'])
    except getopt.GetoptError as error:
        print error
        usage()
    for o, a in opts:
        if o in ('-l', '--list'):
            base_dir = '/sys/bus/w1/devices/'  # point to the address
            device_folder = glob.glob(base_dir + '28*')  # find devices with address starting from 28*
            print device_folder
        elif o in ('-s', '--send'):
            main()
        else:
            usage()
