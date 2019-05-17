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
ON_COLOR = Adafruit_WS2801.RGB_to_color(128,128,128)#64,64,64)#255,255,255)
OFF_COLOR = Adafruit_WS2801.RGB_to_color(0,0,0)

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
	realJson = json.loads(res.text)
	state = realJson["current"]["state"]
	logging.debug("Current printer state is " + state)
	if state=="Operational" or state=="Printing":
		return True
	return False

def setColor(color):
	for i in range(5,pixels.count()):
		pixels.set_pixel(i,color)
	pixels.show()



while True:
	if connected():
		setColor(ON_COLOR)
	else:
		setColor(OFF_COLOR)

	print connected()
	time.sleep(1)
