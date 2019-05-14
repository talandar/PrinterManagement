from __future__ import division
import time
import logging
import json
import requests

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Setup Logging
logging.basicConfig(filename='printController.log',level=logging.DEBUG)
logging.info('Initializing printer controller!')

# Setup LEDs
PIXEL_COUNT = 23
PIXEL_CLOCK = 21
PIXEL_DOUT  = 20
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=PIXEL_CLOCK, do=PIXEL_DOUT)

# Setup Octoprint API/Requests
OCTOPRINT_API_KEY = "398AFD2204874A208CB8EA5FCF1D5E9D"
OCTOPRINT_API_URL = "http://127.0.0.1/api/"
session = requests.Session()
session.headers["X-Api-Key"] = OCTOPRINT_API_KEY
session.headers["Content-Type"] = "application/json"
session.keep_alive = False
logging.info("setup connection?")


def connected():
	res = session.get(OCTOPRINT_API_URL + "connection")
	status = res.status_code
	if status != 200:
		return False
	print res.json()
	realJson = json.loads(res.text)
	state = realJson["current"]["state"]
	print state
	if state=="Operational" or state=="Printing":
		return True
	return False

def blink():
	for i in range(pixels.count()):
		pixels.set_pixel(i,Adafruit_WS2801.RGB_to_color(255,255,255))
	pixels.show()

	time.sleep(5)

	for i in range(pixels.count()):
		pixels.set_pixel(i,Adafruit_WS2801.RGB_to_color(0,0,0))
	pixels.show()

#blink()
while True:
	print connected()
	time.sleep(1)
