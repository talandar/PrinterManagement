# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
 
# Configure the count of pixels:
PIXEL_COUNT = 23
 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
PIXEL_CLOCK = 21
PIXEL_DOUT  = 20
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=PIXEL_CLOCK, do=PIXEL_DOUT)
 
 
for i in range(pixels.count()):
    pixels.set_pixel(i,Adafruit_WS2801.RGB_to_color(255,255,255))
pixels.show()
