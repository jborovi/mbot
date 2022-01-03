'''
Created on Oct 10, 2016

@author: user
'''
from robot.api.controll.EventsManager import EventsManager
from robot.api.hw.GPIO_controll import GPIO_controll
from robot.api import Constants
import sys

class ButtonController(object):
    '''
    classdocs
    big blue button controller
    '''
    
    def __init__(self, gpio_button_pin):
        self.buttonControl = GPIO_controll(gpio_button_pin)

    def wait_for_event_timeout(self, e, t):
        while not e.isSet(): 
#             print 'Button tick'
            event_is_set = e.wait(t)
            if not EventsManager.demoMode.isSet():
                if EventsManager.conversationWaitForButtonHold.isSet():            
                    if self.buttonControl.is_on():
                        EventsManager.trigger_listen_to_user()
                    else:
                        EventsManager.trigger_stop_recording_audio()
                        
                elif EventsManager.sleepMode.isSet() or EventsManager.neutralMode.isSet():                
                    if self.buttonControl.is_on():
                        EventsManager.trigger_converstation_start()
                    

#         print 'Button End'
        sys.exit()            