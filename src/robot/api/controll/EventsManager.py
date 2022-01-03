'''
Created on Sep 29, 2016

@author: user
'''
import threading
from robot.api.Helpers import millis
from __builtin__ import staticmethod

class EventsManager(object):
    '''
    classdocs
    '''
    
    startEvent = threading.Event()

    sleepMode = threading.Event()
    
    neutralMode = threading.Event()
    
    demoMode = threading.Event()
    
    demoModeStart = None
    
    sleepModeStart = None
    
    converstationMode = threading.Event()
    
    converstationStart = threading.Event()
    
    conversationWaitForButtonHold = threading.Event()
    
    conversation_started_time = None
    
    conversation_wait_for_button_time = None
    
    button_is_pressed = threading.Event()
    
    conversationListenToUser = threading.Event()
    
    microphone_record_audio = threading.Event()

    say_hello = threading.Event()
    
#     bigButtonActivated = threading.Event()
    
    
    
    analyze_speech = threading.Event()
    
    endRobot = threading.Event()
    
    @staticmethod
    def trigger_listen_to_user():
        EventsManager.conversationListenToUser.set()
        EventsManager.button_is_pressed.set()
        EventsManager.microphone_record_audio.set()
        
    @staticmethod
    def trigger_stop_recording_audio():        
        EventsManager.microphone_record_audio.clear()
        EventsManager.button_is_pressed.clear()
        EventsManager.conversationListenToUser.clear()
    
    @staticmethod
    def trigger_demo():
        '''
        To turn on the demo mode displaying all emotions in cycle
        '''
        EventsManager.demoModeStart = millis()
        EventsManager.demoMode.set()
        EventsManager.sleepMode.clear()
        EventsManager.neutralMode.clear()
        EventsManager.converstationMode.clear()
        EventsManager.button_is_pressed.clear()
        EventsManager.conversationListenToUser.clear()
#         print 'demp mode activated'
    
    @staticmethod
    def trigger_sleep():
        '''
        To send robot to the sleep state
        '''
#         print 'trigger_sleep'
        EventsManager.demoMode.clear()
        EventsManager.neutralMode.clear()
        EventsManager.sleepMode.set()        
        EventsManager.sleepModeStart = millis()
        EventsManager.say_hello.set()
#         print 'sleep mode activated'
        
    @staticmethod
    def trigger_converstation_start():
#         print 'trigger_converstation_start'
        EventsManager.sleepMode.clear()
        EventsManager.neutralMode.clear()
        EventsManager.converstationMode.set()
        EventsManager.converstationStart.set()
        EventsManager.conversation_started_time = millis()
        
    @staticmethod
    def trigger_conversation_stop():
        '''
        Robot stops conversation
        '''
#         print 'trigger_conversation_stop'
        EventsManager.converstationMode.clear()
        EventsManager.neutralMode.set()
        EventsManager.say_hello.clear()
        EventsManager.converstationStart.clear()
        EventsManager.conversation_started_time = None
        EventsManager.conversationWaitForButtonHold.clear()
        
    @staticmethod
    def trigger_conversation_wait_for_button_hold():
        '''
        Robot will be waiting for big blue button push to start listening, without saying 'Hello'
        '''
#         print 'trigger_conversation_wait_for_button_hold'
        EventsManager.conversationWaitForButtonHold.set()
        EventsManager.converstationStart.clear()
        EventsManager.conversation_wait_for_button_time = millis()
        EventsManager.analyze_speech.clear()
        EventsManager.neutralMode.clear()
    
    @staticmethod
    def trigger_get_emotion_results():
        '''
        To send recorded wav to the Tone analyzer
        '''
#         print 'trigger_send_to_tone_analyzer'
        EventsManager.analyze_speech.set()
        EventsManager.conversationWaitForButtonHold.clear()
        EventsManager.conversationListenToUser.clear()
        EventsManager.neutralMode.clear()
        

    @staticmethod
    def trigger_end_conversation_sleep():
        '''
        Use this if you to send robot to start of the conversation state (robot will be sleeping after motion detection or big blue button push he will say hello and starts listen... 
        '''

        EventsManager.analyze_speech.clear()
        EventsManager.conversationListenToUser.clear()
        EventsManager.trigger_conversation_stop()
        EventsManager.conversationWaitForButtonHold.clear()
        EventsManager.trigger_sleep()
        EventsManager.say_hello.set()
        EventsManager.neutralMode.clear()