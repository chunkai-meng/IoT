# *****************************************************************************
# Copyright (c) 2017 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# *****************************************************************************
import time
import ibmiotf.device
import datetime
from grovepi import *
from grove_rgb_lcd import *

event = "event"
nummsgs = 20		# number of message to send
sensorChoice = 1	# 1: Temperature & Humidity;  -1: Rotary Angle

# Sensor Parameters
dht_sensor_port = 7
dht_sensor_type = 0
potentiometer = 2
button = 4
pinMode(button,"INPUT")

try:
	options = {"org": "1nzzii", "type": "my_device_type",
				"id": "raspberrypi", "auth-method": "token",
				"auth-token": "L6cIl?LVvNKhXZ!0xL"}
	client = ibmiotf.device.Client(options)
except ibmiotf.ConnectionException  as e:
	print e

def captureButtonClick(seconds):
	ifClicked = False
	for i in range(0, 100 * seconds):
		time.sleep(.01)
		if digitalRead(button):
			ifClicked = True
			print("Button Clicked")
			time.sleep(.3)
	return ifClicked

client.connect()

for x in range(0, nummsgs):
	try:
		ang = analogRead(potentiometer) / 4
		[temp, hum] = dht(dht_sensor_port, dht_sensor_type)
		data = {'temp': temp, 'hum': hum, 'ang': ang, 'option': sensorChoice}
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

		def myOnPublishCallback():
			print('{}:\t{}\tTemperature: {}C | Humidity: {}% | ang: {} | option: {}'
				.format(x, st, temp, hum, ang, sensorChoice))
		success = client.publishEvent(event, "json", data, qos=0, on_publish=myOnPublishCallback)

		if not success: print("Not connected to IoTF")
		if captureButtonClick(1): sensorChoice *= -1
	except KeyboardInterrupt as e:
		print(str(e))
		break

client.disconnect()
