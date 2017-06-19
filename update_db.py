#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import sys
import os
import requests

import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
sensor = MAX31855.MAX31855(spi=SPI.SpiDev(0, 0))

table_name = 'temperatures'
api_host = os.getenv('API_HOST', 'localhost:3000')
auth_user = os.getenv('AUTH_USER')
auth_pass = os.getenv('AUTH_PASS')


if auth_user is None:
    sys.exit('AUTH_USER is not set')

if auth_pass is None:
    sys.exit('AUTH_PASS is not set')


def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


def get_temps():
    sensor = MAX31855.MAX31855(spi=SPI.SpiDev(0, 0))
    temp = sensor.readTempC()
    ext = sensor.readInternalC()
    return int(temp), int(ext)


# ###
# RUN
# ###

def run():
    probetemp_c, externaltemp_c = get_temps()
    probetemp_f = c_to_f(probetemp_c)
    externaltemp_f = c_to_f(externaltemp_c)

    if probetemp_f < 100:
        print("< 100F. Not inserting.")
        return

    print("adding record to %s" % api_host)

    data = {'probe_f': int(probetemp_f),
            'probe_c': int(probetemp_c),
            'external_f': int(externaltemp_f),
            'external_c': int(externaltemp_c)}

    resp = requests.post(
        url="%s/api/temperature" % api_host,
        json=data,
        auth=(auth_user, auth_pass)
    )

    if not 200 <= resp.status_code <= 299:
        sys.exit("bad status from API: %s\n\tcontent:%s"
                 % (resp.status_code, resp.content))

    print("Updated temp to %d F" % probetemp_f)
    print("[DEBUG] response: %s" % resp.content)


if __name__ == '__main__':
    run()

