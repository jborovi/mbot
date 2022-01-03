#!/usr/bin/python
# This is only executed on the device client e.g. Raspberry Pi
import time
import os, json
import ibmiotf.application
import uuid
from robot.api.common.common import Common, Observer
import threading
from robot.api import Constants
# import motionSensor



class IOTClient(Observer):
    
    
    DEFAULT_CFG = '/home/honza/robot/cfg/device.cfg'

    client = None

    motionSensorGPIOPort = 4

    number = 0
    
    options = None

    device_id = None
    
    def __init__(self, _config_path):
#         threading.Thread.__init__(self)
        Observer.__init__(self)
        self.config_path = _config_path
        self.running = False
        self._current_event = None


# '/home/honza/usb/x/cfg/device.cfg'
    def connect(self, *args):
        try:
            print 'IOT Connect'
            options = ibmiotf.application.ParseConfigFile(self.config_path)
            options["deviceId"] = options["id"]
            options["id"] = "aaa" + options["id"]
            self.device_id = options['deviceId']
            self.client = ibmiotf.application.Client(options)
            self.client.connect()
        except ibmiotf.ConnectionException as e:
            Common.tty_print(e)
            
    def send_json_msg(self, json_msg):
        try:
            self.client.publishEvent("Raspberry", self.device_id, 'robot_msg', "json", json.dumps(json_msg))
        except ibmiotf.ConnectionException as e:
            Common.tty_print(e)