#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
import collections
Point = collections.namedtuple('Point', ['x', 'y'])

sensor = MAX31855.MAX31855(spi=SPI.SpiDev(0, 0))


def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0

sensor = MAX31855.MAX31855(spi=SPI.SpiDev(0, 0))
temp = sensor.readTempC()
ext = sensor.readInternalC()
probetemp = int(c_to_f(temp))
moduletemp = int(c_to_f(ext))
print('''
  Probe: PROBE
  External: EXTERNAL
'''.replace("PROBE", str(probetemp)).replace("EXTERNAL", str(moduletemp)))
