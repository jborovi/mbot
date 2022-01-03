'''
Created on May 19, 2016
 
@author: user
'''
import logging
from robot.api.controll.EventsManager import EventsManager
import time
from robot.api.controll.ThreadControll import ThreadControll
from robot.api.Helpers import millis
from robot.api.Constants import RANGE_SENSOR_CONTROLL_DELLAY
from robot.api.controll.GUI_EventsManager import GUI_EventsManager
from datetime import datetime
try:
    import RPi.GPIO as GPIO
except Exception:
    print 'MBOT:'+str(datetime.now()) +"GPIO OFF"
 
 
class RangeSensor(object):
    '''
    Range sensor for detecting objects in front of robot
    '''
    
    def __init__(self):
        try:
            import RPi.GPIO as GPIO
            self.SENSOR_ON = True
        except Exception:
            self.SENSOR_ON = False

 
    sendSignal = False
    lastPulseTime = 0
    
    def wait_for_event(self, e):
        pass

    def wait_for_event_timeout(self, e, t):

        while not e.isSet():
#             print 'Range sensor tick'
            event_is_set = e.wait(t)

            if event_is_set:
                logging.debug('processing event')
            else:
                self.get_range_mode(self.get_distance())
        
#         print 'Range sensor end'

                
    def get_range_mode(self, distance):        
        if distance == 0:
            return

        GUI_EventsManager.gui_error_event.text= str(millis())
        if self.getMovement(distance):
            if (EventsManager.sleepMode.isSet() or EventsManager.neutralMode.isSet()) and not EventsManager.demoMode.isSet() and not EventsManager.converstationMode.isSet(): 
                EventsManager.trigger_converstation_start()



    def get_distance(self):
        if self.SENSOR_ON == False:
            return 10
        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            TRIG = 25
            ECHO = 12
            
            import os
    #         from termcolor import colored
    #         tty = os.open("/dev/tty2", os.O_RDWR)        
    # #         os.read(tty, 100) # In separate Thread to be run in parallel
    #         os.write(tty, colored('hello', 'red')) # in main thread
    # #         print 'Distance Measurement In Progress'
            
            GPIO.setup(TRIG,GPIO.OUT)
            GPIO.setup(ECHO,GPIO.IN)
            pulse_start = 0;
            pulse_end = 0;
            distance = 0
            
            self.sendSignal = True
            self.lastPulseTime = 0
            
            while self.sendSignal:
                GPIO.output(TRIG, False)                                                                                                   
            
                time.sleep(0.2)
            
                GPIO.output(TRIG,True)
            
                time.sleep(0.00001)
                GPIO.output(TRIG, False)
                                                                                                                 
                while GPIO.input(ECHO)==0:
                    pulse_start = time.time()
                    if self.lastPulseTime == 0:
                        self.lastPulseTime = pulse_start
                    
                    if pulse_start - self.lastPulseTime > 0.1:
                        self.lastPulseTime = 0
                        break
                                                                                                                        
                while GPIO.input(ECHO)==1:
                    self.sendSignal = False
                    pulse_end = time.time()
            
                pulse_duration = pulse_end - pulse_start
            
                if pulse_duration > 0.000001 and pulse_duration < 0.02:
                    distance = ((pulse_duration*1000000)/2) / 29;
                    distance = round(distance, 2)
                return distance

     
    def getMovement(self, distance):
        return distance > 10 and distance < 100
    
    def get_demo_mode_trigger(self, distance):
        return distance > 1 and distance < 50
          
