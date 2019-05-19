from __future__ import division
from gpiozero import Button
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
homeXYCommand = '{"command": "home","axes": ["x", "y"]}'
pauseCommand = '{"command": "pause"}'

logging.info("setup connection")

# Seup Button
button = Button(13)

def status():
	res = session.get(OCTOPRINT_API_URL + "connection")
	status = res.status_code
	if status != 200:
		return False
	realJson = json.loads(res.text)
	state = realJson["current"]["state"]
	return state

def connected(state):
	if state=="Operational" or state=="Printing" or state=="Paused":
		return True
	return False

def printing(state):
	if state=="Printing":
		return True
	return False

def filamentPresent():
	return button.is_held


def setColor(color):
	for i in range(5,pixels.count()):
		pixels.set_pixel(i,color)
	pixels.show()

def pausePrint():
	print "pause"
	session.post(OCTOPRINT_API_URL+"job",data=pauseCommand)

def goXYHome():
	print "gohome"
	session.post(OCTOPRINT_API_URL+"printer/printhead",data=homeXYCommand)



def filament_out_detected():

	print "out!"
	state = status()
	if printing(state):
		print "out and printing!"
		pausePrint()
		time.sleep(10)
		goXYHome()



button.when_released = filament_out_detected
while True:
	state = status()
	if connected(state):
		setColor(ON_COLOR)
	else:
		setColor(OFF_COLOR)
	time.sleep(1)

