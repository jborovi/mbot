'''
Created on May 19, 2016
 
@author: user
'''
from robot.api.common.common import Observer

try:
    import RPi.GPIO as GPIO
except Exception, e:
    print e

import time
import threading
 
 
class RangeSensor(threading.Thread, Observer):
    '''
    classdocs
    '''
 
    sendSignal = False
    lastPulseTime = 0
    
    current_range = None
    
    def __init__(self):
        threading.Thread.__init__(self)
        Observer.__init__(self)
         
    def get_distance(self):
        return 22
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        TRIG = 23
        ECHO = 24
        
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        pulse_start = 0;
        pulse_end = 0;
        distance = 0
        
        self.sendSignal = True
        self.lastPulseTime = 0
        
        while self.sendSignal:
            GPIO.output(TRIG, False)
        #    print 'Waiting For Sensor To Settle'                                                                                                   
        
            time.sleep(0.2)
        
            GPIO.output(TRIG,True)
        
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
        
        #    print 'Waiting for pulse to start'                                                                                                     
            while GPIO.input(ECHO)==0:
#                 0.1
                pulse_start = time.time()
                if self.lastPulseTime == 0:
                    self.lastPulseTime = pulse_start
                
                if pulse_start - self.lastPulseTime > 0.1:
                    self.lastPulseTime = 0
                    break
                
        
        #    print 'Waiting for pulse to stop'                                                                                                      
            while GPIO.input(ECHO)==1:
                self.sendSignal = False
                pulse_end = time.time()
        
            pulse_duration = pulse_end - pulse_start
        
            if pulse_duration > 0.000001 and pulse_duration < 0.02:
                distance = ((pulse_duration*1000000)/2) / 29;
                distance = round(distance, 2)
#                 print "Distance: ", distance ,"cm"
            return distance
        
    def kill_thread(self, *args):
        print 'kill thread'
        if self.is_alive():
            self.running = False

     
    @staticmethod
    def getMovement(self, distance):
#         distance = self.get_distance()
#         print distance
        return distance >= 21 and distance < 180
    
    @staticmethod
    def get_demo_mode_trigger(distance):
#         distance = self.get_distance()
#         print distance
        return distance > 1 and distance <= 20
    
    def run (self):
        self.running = True
        while self.running:
            self.current_range = self.get_distance()
