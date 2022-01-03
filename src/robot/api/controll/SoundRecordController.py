'''
Created on Oct 12, 2016

@author: user
'''
from robot.api.controll.ThreadControll import ThreadControll
from robot.api.controll.EventsManager import EventsManager
from robot.api import Constants
import sys

class SoundRecordController(ThreadControll):

    def __init__(self, sound_mgr):
        '''
        Microphone input record controller, starts recording
        SoundMgr2.py is stopping the recording
        '''
        self.sound_mgr = sound_mgr

    def wait_for_event_timeout(self, e, t):
        while not e.isSet():
#             print 'Sound Record tick'
#             print 'Demo mode tick' 
            demo_mode_count = 0
            event_is_set = e.wait(t)
            
            if EventsManager.conversationListenToUser.isSet():
                self.sound_mgr.record_to_file(Constants.WAW_RECORD_INPUT)
#         print 'Sound Record End'
        sys.exit()
            