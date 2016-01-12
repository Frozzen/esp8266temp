#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    получаем температуру c DS1802 и отправляем ее на thingspeak.com

    RPI: работаем на старом ядре 3.14.х ядро 4.х парит
    usage:
        python things.py --send=AOSNEW2 померить и отослать температуру
        python things.py --list показать список термометров и температуры

    пример кода
    http://stackoverflow.com/questions/30889872/how-to-post-api-in-thingspeak-comusing-urllib-in-python
    https://electrosome.com/ds18b20-sensor-raspberry-pi-python/
"""
import urllib
import httplib
import glob
import time
import getopt, sys

__1wire = '/sys/bus/w1/devices/'
__1w_device = '/temperature'

# массив для перекодировки устройство -> поле в thingspeak
__device_table = {
    '28-0000054822f5': 'field1',
    '28-000005482a81': 'field2',
    '.': 'field3',
    '.': 'field4'
}

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()  # read the device details
    f.close()
    return lines


def read_temp(device_file):
    lines = read_temp_raw(device_file + '/w1_slave')
    while lines[0].strip()[-3:] != 'YES':  # ignore first line
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')  # find temperature in the details
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0  # convert to Celsius
        return temp_c
    return None


def readAll(device_folders):
    """
    прочитать все датчики

    :rtype : dict {dev_file: value}
    :param device_folders:
    :return:
    """
    res = {}
    for device_folder in device_folders:
        res[device_folder] = read_temp(device_folder)
    return res


def sendTemp(temps, tkey):
    """
    перекодировать температуры и послать их на thingspeak
    :type temps: dict
    :param key: thingspeak.com channel KEY
    :param temps: dict устройство - температура
    :return:
    """
    # http://184.106.153.149
    urlparams = {}
    for key in temps:
        k = key.split('/')[-1]
        if k in __device_table and not (temps[key] is None):
            urlparams[__device_table[k]] = temps[key]
    if len(urlparams) == 0:
        return
    urlparams['key'] = tkey

    params = urllib.urlencode(urlparams)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("184.106.153.149:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            print response.status, response.reason
            data = response.read()
        conn.close()
    except httplib.HTTPException as e:
        print "connection failed", e


def main(key):
    device_folder = glob.glob(__1wire + '28*')  # find devices with address starting from 28*

    res = readAll(device_folder)
    sendTemp(res, key)


def usage():
    print __doc__
    sys.exit(1)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:l', ['send=', 'list'])
    except getopt.GetoptError as error:
        print error
        usage()
    for o, a in opts:
        if o in ('-l', '--list'):
            device_folder = glob.glob(__1wire + '28*')  # find devices with address starting from 28*
            print("device attached:")
            for d in device_folder:
                t = read_temp(d)
                print("dev:%s temp:%5.2f" % (d.split('/')[-1], t))
        elif o in ('-s', '--send'):
            main(a)
        else:
            usage()
