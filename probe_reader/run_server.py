#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
import collections
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

Point = collections.namedtuple('Point', ['x', 'y'])
sensor = MAX31855.MAX31855(spi=SPI.SpiDev(0, 0))


def c_to_f(c):
    """
    convert celcius to fahrenheit
    """
    return c * 9.0 / 5.0 + 32.0


class S(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        GET is for the browser
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        t = get_temps()
        self.wfile.write('<html><body>')
        self.wfile.write('<div style="font-size: 26px !important; color: black; width: 50% !important;">')
        self.wfile.write('Probe: ' + str(t.x) + '</br>')
        self.wfile.write('External: ' + str(t.y))
        self.wfile.write('</div>')
        self.wfile.write('</body></html>')


    def do_POST(self):
        """
        POST is from Alexa
        """
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        t = get_temps()
        self.wfile.write('''{
          "response": {
            "outputSpeech": {
              "type": "PlainText",
              "text": "internal PROBE degrees, external EXTERNAL degrees"
            },
            "shouldEndSession": true
          },
          "sessionAttributes": {}
        }'''.replace("PROBE", str(t.x)).replace("EXTERNAL", str(t.y)))


def get_temps():
    SPI_PORT = 0
    SPI_DEVICE = 0
    sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    temp = sensor.readTempC()
    ext = sensor.readInternalC()
    return Point(int(c_to_f(temp)), int(c_to_f(ext)))


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(port=3000)
