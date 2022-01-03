'''
Created on Oct 5, 2016

@author: user
'''
from robot.api.controll.ThreadControll import ThreadControll
from robot.api.controll.EventsManager import EventsManager
from robot.api import Constants
from robot.api.Helpers import millis
from robot.api.net.NetCom import NetCom
from speech_recognition import UnknownValueError
import time
from robot.api.controll.GUI_EventsManager import GUI_EventsManager
from datetime import datetime
import sys

class ConversationFlowController(ThreadControll):
    
    
    WAIT_FOR_BUTTON_TIME = 30000
    
    conversation_count = 0

    def __init__(self, sound_mgr_ref, adruino):
        self.sound_mgr = sound_mgr_ref
        self.adruino = adruino
        self.netcom = NetCom()
        self.flag_analyzing = False
        
    def wait_for_event(self, e):
        pass
#           super(ConversationFlowController, self).wait_for_event(e)         
    
    
    def wait_for_event_timeout(self, e, t):
#         super(DemoModeController,self).wait_for_event_timeout(e, t)
            while not e.isSet(): 
#                 print 'Conversation tick'
                demo_mode_count = 0
                event_is_set = e.wait(t)
                if EventsManager.converstationMode.isSet():
                    if EventsManager.converstationStart.isSet():
                        self.adruino.write_emotion('neutral')
                        if EventsManager.say_hello.isSet():
                            self.sound_mgr.play_wav(Constants.WAW_GREETING_F)                        
                        EventsManager.trigger_conversation_wait_for_button_hold()
                        self.conversation_count = 1
                    elif EventsManager.conversationWaitForButtonHold.isSet():
                        if EventsManager.button_is_pressed.isSet():
                            self.adruino.write_emotion('neutral')
                            GUI_EventsManager.clear_conv_results()                            
                        if self.conversation_count > 2:
                            EventsManager.trigger_end_conversation_sleep()
                            EventsManager.trigger_sleep()
                            self.conversation_count = 0
                        elif millis() - EventsManager.conversation_wait_for_button_time > self.WAIT_FOR_BUTTON_TIME:
                            self.conversation_count += 1 
                            EventsManager.conversation_wait_for_button_time =  millis()
                            self.adruino.write_emotion('neutral')
                            
#                             self.conversation_started_time = millis()
                            if EventsManager.say_hello.isSet():
                                self.sound_mgr.play_wav(Constants.WAW_GREETING_F)

                    elif EventsManager.analyze_speech.isSet(): #and not self.flag_analyzing:
#                         self.flag_analyzing = True
                        self.sound_mgr.play_wav(Constants.MSG_CONTINUE_CONF_F, False)
                        try:
                            recognized_sound  = self.netcom.recognize(Constants.WAW_RECORD_INPUT)
                            
#                             GUI_EventsManager.conversation_text_recognized.
                            if recognized_sound is not None:
                                recognized_sound = " ".join(recognized_sound.split())
                            GUI_EventsManager.conversation_text_recognized.text = recognized_sound
                        except UnknownValueError, uve:
                            GUI_EventsManager.conversation_text_recognized.text = "Sorry I did understand nothing. :("
                            time.sleep(2)
                            print 'MBOT:'+(str(datetime.now()) + 'Sensor did not understand, or nobody spoke')

                            self.adruino.write_emotion('fear')
                            self.sound_mgr.play_wav(Constants.MSG_DONT_UNDERSTAND_F)
                            EventsManager.trigger_conversation_wait_for_button_hold()
                            EventsManager.say_hello.clear()
                            continue
                        except Exception, exc1:
                            GUI_EventsManager.conversation_text_recognized.text = "Sorry there was unexpected error, pls check the error log or restart me :("
                            time.sleep(2)
                            print 'MBOT:'+(str(datetime.now()) + 'Recognize, error: '+str(exc1))

                            self.adruino.write_emotion('fear')
                            self.sound_mgr.play_wav(Constants.MSG_DONT_UNDERSTAND_F)
                            EventsManager.trigger_conversation_wait_for_button_hold()
                            EventsManager.say_hello.clear()
                            continue
                        
                        try:
                            self.netcom.analyzed_emotion = self.netcom.analyze(recognized_sound)                                                                        
                            self.adruino.write_emotion(self.netcom.analyzed_emotion)
                            self.netcom.set_reply_wav(self.netcom.analyzed_emotion)    
                            self.sound_mgr.play_wav(self.netcom.emotion_wav)
    #                         self.flag_analyzing = False
                            EventsManager.say_hello.clear()
                            EventsManager.trigger_conversation_wait_for_button_hold()
                        except Exception, exc2:
                            GUI_EventsManager.conversation_text_recognized.text = "Sorry there was unexpected error, pls check the error log or restart me :("
                            time.sleep(2)
                            print 'MBOT:'+(str(datetime.now()) + 'Recognize, error: '+str(exc2))

                            self.adruino.write_emotion('fear')
                            EventsManager.trigger_conversation_wait_for_button_hold()
                        
            sys.exit()