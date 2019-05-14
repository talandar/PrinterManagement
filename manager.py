from __future__ import division
import time
import logging

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Setup Logging
logging.basicConfig(filename='printController.log',level=logging.DEBUG)
logging.info('Initializing printer controller!')


# Configure the count of pixels:
PIXEL_COUNT = 23

# The WS2801 library makes use of the BCM pin numbering scheme. See the README.md for details.

# Specify a software SPI connection for Raspberry Pi on the following pins:
PIXEL_CLOCK = 21
PIXEL_DOUT  = 20
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=PIXEL_CLOCK, do=PIXEL_DOUT)

for i in range(pixels.count()):
    pixels.set_pixel(i,Adafruit_WS2801.RGB_to_color(255,255,255))
pixels.show()

time.sleep(5)

for i in range(pixels.count()):
    pixels.set_pixel(i,Adafruit_WS2801.RGB_to_color(0,0,0))
pixels.show()