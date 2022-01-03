'''
Created on Sep 29, 2016

@author: user
'''
from robot.api.controll.ThreadControll import ThreadControll
from robot.api.controll.EventsManager import EventsManager
import time
from robot.api import Constants
import sys

class DemoModeController(ThreadControll):

    def __init__(self, adruino_ref, sound_mgr_ref, demo_delay):
        self.adruino = adruino_ref
        self.soundMgr = sound_mgr_ref
        self.demo_delay = demo_delay

    def wait_for_event_timeout(self, e, t):
#         super(DemoModeController,self).wait_for_event_timeout(e, t)
        while not e.isSet(): 
#             print 'Demo mode tick'
            demo_mode_count = 0
            event_is_set = e.wait(t)
            if EventsManager.demoMode.isSet():
#                 demo_last_triggered = time.time()
                    
#                 if demo_mode_count == 0:# or ((time.tim/e() - demo_last_triggered) > Constants.ROBOT_DEMO_MODE_PERIOD):
#                     demo_last_triggered = time.time()
#                 if demo_mode_count == 0:
#                     self.soundMgr.play_wav(Constants.WAV_DEMO_MODE_F)
                    
                demo_mode_count += 1
#                     demo_mode_count += 1

#               self.adruino.write_emotion('wakeup')                
                self.show_emotion('wakeup')
                self.show_emotion('neutral')
                self.show_emotion('anger')
                self.show_emotion('disgust')
                self.show_emotion('fear')
                self.show_emotion('joy')                
                self.show_emotion('sleep')
#         print 'Demo mode end'
        sys.exit()
                
    def show_emotion(self, emotion):        
        if EventsManager.demoMode.isSet():
            self.adruino.write_emotion(emotion)            
            time.sleep(self.demo_delay)

    