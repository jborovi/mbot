'''
Created on Jul 7, 2016

@author: user
'''
import threading
from robot.api.common.common import Observer
from robot.api.common.common import Event
from robot.api.iot.iotClient import IOTClient
from robot.api import Constants
import time
import Queue
from robot.api.hw.RangeSensor import RangeSensor
from robot.api.hw.adruinoConnect import AdruionConnect
from robot.api.hw.GPIO_controll import GPIO_controll

class MainController(threading.Thread, Observer):
    IOT_ON = True
    SENSOR_ON = True
    EMOTION_OUTPUT = True
    
    threads = []
    
    current_state = None
    
    convesation_state = None
    
    ST_DEMO = 1
    ST_NORMAL = 2
    
    C_ST_STARTED = 1
    C_ST_ANALYZING = 2
    C_ST_RESPONSE = 3
    
    def __init__(self):
        threading.Thread.__init__(self)
        Observer.__init__(self)
        
        self.running = False
        if MainController.IOT_ON:
            self.iotClient = IOTClient("C:\\Development\\Projects\\Python\\SpeechApi\\cfg\\device.cfg")
            self.iotClient.observe(Constants.IOT_CONNECT, self.iotClient.connect)
        
        if self.SENSOR_ON:
            self.range_sensor = RangeSensor()
            self.range_sensor.observe(Constants.EVENT_KILL, self.range_sensor.kill_thread)
            
        if self.EMOTION_OUTPUT:
            self.adruino = AdruionConnect('/dev/ttyACM0', 9600)
            self.adruino.observe(Constants.EVENT_WAKE_UP, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_SLEEP, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_NEUTRAL, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_ANGER, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_DISGUST, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_SADNESS, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_FEAR, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_SCARED, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_JOY, self.adruino.event_listener)
            self.adruino.observe(Constants.EVENT_SLEEP, self.adruino.event_listener)
            
        self.buttonControl = GPIO_controll(Constants.GPIO_button_pin)
        self.buttonControl.observe(Constants.EVENT_KILL, self.buttonControl.kill_thread)
        
            
        threads.append(self.range_sensor)
        threads.append(self.buttonControl)
#         for t in threads:
#             if t.is_alive():
#                 t.join()


    def event_listener(self, event_name):
        if event_name == Constants.EVENT_KILL:
            print 'kill thread'
            if self.is_alive():
                self.running = False
                
        if event_name == Constants.EVENT_DEMO_MODE:
            self.convesation_state = False
#         elif event_name == Constants.EVENT_SLEEP:
#             self.range_sensor_state = self.ST_NORMAL
        if event_name == Constants.EVENT_WAKE_UP:
            self.convesation_state = self.C_ST_STARTED
        else:
            self.current_state = event_name
#             self.convesation_state = self.ST_NORMAL
        
    def run(self):
        self.running = True
        if MainController.IOT_ON:
            while self.running:
                print 'run'
#                 threadLock.acquire()    
                print self.running
                time.sleep(1)
#                 threadLock.release()  
               
                print self.current_state
                if self.current_state == Constants.EVENT_INIT:
                    if not self.range_sensor.is_alive():
                        self.range_sensor.start()
                        Event(Constants.EVENT_SLEEP,Constants.EVENT_SLEEP)
                        
                elif self.current_state == Constants.EVENT_NORMAL_MODE:
                    print 'range det'
                    print self.range_sensor.current_range
                    self.range_sensor.join()
                    if RangeSensor.get_demo_mode_trigger(self.range_detected):
                        if self.convesation_state == False:
                            Event(Constants.EVENT_DEMO_MODE, Constants.EVENT_DEMO_MODE)
                    elif RangeSensor.getMovement(self.range_detected):
                        if self.convesation_state == False:
                            Event(Constants.EVENT_WAKE_UP, Constants.EVENT_WAKE_UP)

            

if __name__ == '__main__':
#     threadLock = threading.Lock()
    threads = []    
    mainC = MainController()    
    mainC.start()
#     mainC.join()
    mainC.observe(Constants.EVENT_KILL, mainC.event_listener)
    mainC.observe(Constants.EVENT_INIT, mainC.event_listener)
    mainC.observe(Constants.EVENT_NORMAL_MODE, mainC.event_listener)
    mainC.observe(Constants.EVENT_DEMO_MODE, mainC.event_listener)
    
    
    threads.append(mainC)
    
#     for t in threads:
#         t.join()
        
    Event(Constants.EVENT_INIT,Constants.EVENT_INIT)
#     
    
#     Event(Constants.IOT_CONNECT,None)
        
    
    