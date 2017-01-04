#!/usr/bin/env python

import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
import collections
import sqlite3
from datetime import datetime

Point = collections.namedtuple('Point', ['x', 'y'])
sensor = MAX31855.MAX31855(spi=SPI.SpiDev(0, 0))

# ##
# Variables
# ##
db_file = '../temperatures.db'
table_name = 'temperatures'


def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


def get_temps():
    sensor = MAX31855.MAX31855(spi=SPI.SpiDev(0, 0))
    temp = sensor.readTempC()
    ext = sensor.readInternalC()
    return int(temp), int(ext)


def tableExists(con):
    c = con.cursor()
    c.execute("""SELECT COUNT(1) FROM sqlite_master WHERE name=? and type='table';""", (table_name,))
    if c.fetchone()[0] == 1:
        c.close()
        return True
    c.close()
    return False


# ###
# RUN
# ###
conn = sqlite3.connect(db_file)

# Create table if not exist
if tableExists(conn) is False:
    print("table does not exist")
    c = conn.cursor()
    c.execute('''
              CREATE TABLE temperatures
              (probe_f integer, external_f integer, probe_c integer, external_c integer, modified date)
              ''')
    print("table created")
    c.close()


probetemp_c, externaltemp_c = get_temps()
probetemp_f = c_to_f(probetemp_c)
externaltemp_f = c_to_f(externaltemp_c)

# Insert a row of data
c = conn.cursor()
c.execute("""
          INSERT INTO temperatures
          (probe_f, probe_c, external_f, external_c, modified)
          VALUES (?,?,?,?,?)
          """,
          (probetemp_f, probetemp_c, externaltemp_f, externaltemp_c, datetime.utcnow()))

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

