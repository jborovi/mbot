#!/usr/bin/python
# This is only executed on the device client e.g. Raspberry Pi
import time
import os, json
import ibmiotf.application
import uuid
from robot.api.common.common import Common
# import motionSensor



class IOTClient():
    
    
    DEFAULT_CFG = '/home/honza/robot/cfg/device.cfg'

    client = None

    motionSensorGPIOPort = 4

    number = 0
    
    options = None
	
    device_id = None


# '/home/honza/usb/x/cfg/device.cfg'
    def connect(self, config_path):
        try:
            options = ibmiotf.application.ParseConfigFile(config_path)
            options["deviceId"] = options["id"]
            options["id"] = options["id"]
            self.device_id = options['deviceId']
            self.client = ibmiotf.application.Client(options)
#             print options
#             print "try to connect to IoT"
            self.client.connect()
#             print self.client
#             print "connect to IoT successfully"
        
#             motionStatus = False
        #     motionSensor.setup(motionSensorGPIOPort)
        
        #  motionData = motionSensor.sample()
        #  jsonMotionData = json.dumps(motionData)
#         	client.publishEvent("Raspberry", options["deviceId"], "motionSensor", "json", json.dumps({"motionDetected":number}))
                
                
#                 time.sleep(0.2)
        except ibmiotf.ConnectionException as e:
            Common.tty_print(str(e))
            
    def send_json_msg(self, json_msg):
        try:
            self.client.publishEvent("RaspberryPi", self.device_id, 'robot_msg', "json", json.dumps(json_msg))
#             print "publish"
        except ibmiotf.ConnectionException as e:
            Common.tty_print(str(e))
