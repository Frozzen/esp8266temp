#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    получаем температуру c DS1802 и отправляем ее на thingspeak.com
    RPI:
    usage:
        python things.py --send померить и отослать температуру
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

__1wire = '/mnt/1wire/'
__1w_device = '/temperature'
__device_table = {
    '.' : 'field1',
    '.' : 'field2',
    '.' : 'field3',
    '.' : 'field4'
}

def read_temp_raw(device_file):
    """

    :type device_file: str folder to owfs device
    :return:
    """
    f = open(device_file+__1w_device, 'r')
    lines = f.read()  # read the device details
    f.close()
    return lines


def read_temp(dev):
    """
    прочитать температуру и конвертировать
    :param dev:
    :return:
    """
    temp_string = read_temp_raw(dev)
    temp_c = float(temp_string.strip())   # convert to Celsius
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
        res[device_folder] = read_temp(device_folder)
    return res


def sendTemp(temps):
    """
    перекодировать температуры и послать их на thingspeak
    :param temps:
    :return:
    """
    # chanId: 74111; field[1-4]:room1temp, hotWaterTemp, coldWaterTemp, tempOutside
    # http://184.106.153.149
    urlparams = {}
    for key in temps:
        k = key.split('/')[-1]
        if k in __device_table and not (temps[key] is None):
            urlparams[__device_table[k]] = temps[key]
    if len(urlparams) == 0:
        return
    urlparams['key'] = 'IL6Q4TBCJGSA9CVF'

    params = urllib.urlencode(urlparams)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("184.106.153.149:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
    except Exception as e:
        print "connection failed", e


def main():
    device_folder = glob.glob(__1wire + '10*')  # find devices with address starting from 28*

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
            base_dir = __1wire  # point to the address
            device_folder = glob.glob(base_dir + '10*')  # find devices with address starting from 28*
            print("device attached:")
            for d in device_folder:
                t = read_temp(d)
                print("dev:%s temp:%5.2f\n" % (d.split('/')[-1], t))
        elif o in ('-s', '--send'):
            main()
        else:
            usage()
