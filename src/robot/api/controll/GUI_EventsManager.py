'''
Created on Oct 24, 2016

@author: user
'''
# from threading import Event
from threading import _Event

class TextEvent (_Event):

    def __init__(self, text):
        super(TextEvent, self).__init__()
        self.text = text
        
    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, t):
        self.__text = t

class GUI_EventsManager(object):
    
    
    '''
    Variables needed to display in the LCD ui
    '''

    gui_error_event = TextEvent(None)
    
    ip_address_event = TextEvent(None)

    conversation_text_recognized = TextEvent(" ")
    
    conversation_tone_result = TextEvent("")
    conversation_tone_result_joy = TextEvent("")
    conversation_tone_result_fear = TextEvent("")
    conversation_tone_result_disgust = TextEvent("")
    conversation_tone_result_anger = TextEvent("")
    conversation_tone_result_sadness = TextEvent("")
    
    
    @staticmethod
    def clear_conv_results():
        GUI_EventsManager.conversation_tone_result.text = ""
        GUI_EventsManager.conversation_text_recognized.text = ""
        GUI_EventsManager.conversation_tone_result_joy.text = ""
        GUI_EventsManager.conversation_tone_result_fear.text = ""
        GUI_EventsManager.conversation_tone_result_disgust.text = ""
        GUI_EventsManager.conversation_tone_result_anger.text = ""
        GUI_EventsManager.conversation_tone_result_sadness.text = ""