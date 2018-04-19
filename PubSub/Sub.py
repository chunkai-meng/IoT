# *****************************************************************************
# Copyright (c) 2014 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#   David Parker - Initial Contribution
# *****************************************************************************
import getopt
import signal
import time
import sys
import json
import ibmiotf.application
from grovepi import *
from grove_rgb_lcd import *

tableRowTemplate = "%-33s%-30s%s"
deviceType = "+"
deviceId = "+"
event = "+"

def mySubscribeCallback(mid, qos):
    if mid == statusMid:
        print("<< Subscription established for status messages at qos %s >> " % qos[0])
    elif mid == eventsMid:
        print("<< Subscription established for event messages at qos %s >> " % qos[0])


def myEventCallback(event):
    if event.data['option'] == 1:
    	setText_norefresh("Temp: {}C\nHumidity: {}%".format(event.data['temp'], event.data['hum']))
    else:
     	setText_norefresh("Angle: {}  ".format(event.data['ang']))
    print event.data

def myStatusCallback(status):
    if status.action == "Disconnect":
        summaryText = "%s %s (%s)" % (status.action, status.clientAddr, status.reason)
    else:
        summaryText = "%s %s" % (status.action, status.clientAddr)
    print(tableRowTemplate % (status.time.isoformat(), status.device, summaryText))


def interruptHandler(signal, frame):
    client.disconnect()
    setText("")
    sys.exit(0)


client = None
options = {"org": "1nzzii", "id": "myApplication", "auth-method": "apikey",
            "auth-key": "a-1nzzii-zmgugzhj3q", "auth-token": "e**ai?sigv)NkkOKf9"}
try:
    client = ibmiotf.application.Client(options)
    # import logging
    # client.logger.setLevel(logging.DEBUG)
    client.connect()
except ibmiotf.ConfigurationException as e:
    print(str(e))
    sys.exit()
except ibmiotf.UnsupportedAuthenticationMethod as e:
    print(str(e))
    sys.exit()
except ibmiotf.ConnectionException as e:
    print(str(e))
    sys.exit()

print("(Press Ctrl+C to disconnect)")
dht_sensor_port = 7
dht_sensor_type = 0
setRGB(0,255,0)

client.deviceEventCallback = myEventCallback
client.deviceStatusCallback = myStatusCallback
client.subscriptionCallback = mySubscribeCallback

eventsMid = client.subscribeToDeviceEvents(deviceType, deviceId, event)
statusMid = client.subscribeToDeviceStatus(deviceType, deviceId)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt as e:
        break
