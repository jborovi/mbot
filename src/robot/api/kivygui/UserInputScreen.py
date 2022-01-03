from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button, Label
from robot.api.controll.EventsManager import EventsManager
from robot.api.controll.GUI_EventsManager import GUI_EventsManager
from kivy.core.audio.audio_sdl2 import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

FONT_SIZE_DEMO = 30

FONT_SIZE = 25

RESULT_FONT_SIZE = 20

RESULT_FONT_SIZE_2 = 18

RESULT_FONT_SIZE_3 = 15


TXT_DEMO_ON = "Activate Demo Mode"
TXT_DEMO_OFF = 'Deactivate Demo Mode'


        
        

class MenuScreen(FloatLayout):
    
        TXT_IP = 'MBot IP: '
        
        TXT_STATUS = 'Status: '
        
        TXT_SLEEPING = 'Sleeping. Wake me up with the blue button.'
        
        TXT_WAITING_FOR_BUTTON = 'Hold the blue button and speak.'
        
        TXT_DEMO = 'IN DEMO MODE.'
        
        TXT_ANALYZING = 'Analyzing conversation.'
        
        TXT_LAST_CONV_RES = 'Latest conversation results:'

        def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
            super(MenuScreen, self).__init__(**kwargs)
            
            self.label_up = Label(text='Hello, I am MBot here is my IP:',pos_hint={'x': 0.4, 'y': 0.9}, size_hint=(1, 0.1), bold=True, font_size = 15)

            self.label_status = Label(text=MenuScreen.TXT_STATUS, pos_hint={'x': 0, 'y': 0.8}, size_hint=(1, 0.2), bold=True, font_size = FONT_SIZE)
#             self.label_status2 = Label(pos_hint={'x': 0, 'y': 0.8}, size_hint=(1, 0.1), font_size = FONT_SIZE)
            
            self.label_last_result=Label(text=MenuScreen.TXT_LAST_CONV_RES, pos_hint={'x': 0, 'y': 0.75}, size_hint=(1, 0.1), font_size = FONT_SIZE)
            
            self.label_conversation_txt = Label(text="", pos_hint={'x': 0, 'y': 0.5}, size_hint=(1, 0.3), font_size = FONT_SIZE)
            self.label_conversation_txt.text_size=(700, None)
            self.label_last_conversation_results = Label(pos_hint={'x': 0, 'y': 0}, size_hint=(1, 0.3), font_size = FONT_SIZE)
            self.label_last_conversation_results.text_size=(700, None)
#             tone_res = "Disgust - 200% /t Joy: 0% /n Anger - 0% Fear: 0% /t Sadness - 0%"
#             self.label_last_conversation_results.text=tone_res
            self.btn_demo_mode = Button(text=TXT_DEMO_ON, pos_hint={'right': 1, 'center_y': 0.1},size_hint=(1, 0.2), font_size = FONT_SIZE, bold=True)
            self.btn_demo_mode.background_color = (0.0, 1.0, 0.0, 4)
#             self.btn_demo_mode.background_down = '/home/mbot/mbotProject/res/img/button.png'
            self.btn_demo_mode.background_down = '/home/mbot/mbotProject/res/img/button.png'
            self.label_disgust = Label(text='', pos_hint={'x': 0, 'y': 0.3}, size_hint=(0.5, 0.1), font_size = FONT_SIZE, markup=True)
            self.label_joy =Label(text='', pos_hint={'x': 0.5, 'y': 0.4}, size_hint=(0.5, 0.1), font_size = FONT_SIZE, markup=True)
            self.label_fear =Label(text='', pos_hint={'x': 0, 'y': 0.4}, size_hint=(0.5, 0.1), font_size = FONT_SIZE, markup=True)
            self.label_sadness =Label(text='', pos_hint={'x': 0.5, 'y': 0.3}, size_hint=(0.5, 0.1), font_size = FONT_SIZE, markup=True)
            self.label_anger =Label(text='', pos_hint={'x': 0, 'y': 0.2}, size_hint=(0.5, 0.1), font_size = FONT_SIZE, markup=True)
            
            self.bg_img = Image(source='/home/mbot/mbotProject/res/img/watson.png')
            self.bg_img.allow_stretch = False
            self.add_widget(self.bg_img)
            self.add_widget(self.label_up)
            self.add_widget(self.label_status)
#             self.add_widget(self.label_status2)
            self.add_widget(self.label_last_result)
            self.add_widget(self.label_conversation_txt)  
            self.add_widget(self.label_disgust)          
            self.add_widget(self.label_joy)
            self.add_widget(self.label_fear)
            self.add_widget(self.label_sadness)
            self.add_widget(self.label_anger)
            self.add_widget(self.btn_demo_mode)
            self.btn_demo_mode.bind(on_press=self.auth)
            
        def auth(self, instance):
            if EventsManager.demoMode.isSet():
                EventsManager.trigger_end_conversation_sleep()
                self.btn_demo_mode.text = TXT_DEMO_OFF
            else:
                EventsManager.trigger_demo()
                self.btn_demo_mode.text= TXT_DEMO_ON


class MainApp(App):
    
    def build(self):
#         self.root = root = InputScreen()
        self.root = root = MenuScreen()
        root.bind(size=self._update_rect, pos=self._update_rect)
        Clock.schedule_interval(self.consume, 1)

        with root.canvas.before:
            Color(0, 0, 1, 0.5)  # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def consume(self, *args):
        if GUI_EventsManager.ip_address_event.text is not None:
            self.root.label_up.text = MenuScreen.TXT_IP+str(GUI_EventsManager.ip_address_event.text)
            
        if EventsManager.neutralMode.isSet():
            status_txt = MenuScreen.TXT_WAITING_FOR_BUTTON
        if EventsManager.sleepMode.isSet():
            status_txt = MenuScreen.TXT_SLEEPING
        elif EventsManager.conversationWaitForButtonHold:
            status_txt = MenuScreen.TXT_WAITING_FOR_BUTTON
        if EventsManager.demoMode.isSet():
            status_txt = MenuScreen.TXT_DEMO
            self.root.label_status.font_size = FONT_SIZE_DEMO
        else:
            self.root.label_status.font_size = FONT_SIZE
            
        if EventsManager.analyze_speech.isSet():
            status_txt = MenuScreen.TXT_ANALYZING
            
            
            
        if EventsManager.demoMode.isSet():
            self.root.btn_demo_mode.text = TXT_DEMO_OFF
        else:
            self.root.btn_demo_mode.text= TXT_DEMO_ON
        
        self.root.label_status.text = MenuScreen.TXT_STATUS + " " + status_txt
        
        
        if EventsManager.demoMode.isSet():    
            self.root.label_last_result.text = "";
            self.root.label_conversation_txt.text = "";
            self.root.label_disgust.text = "";
            self.root.label_joy.text ="";
            self.root.label_fear.text ="";
            self.root.label_sadness.text ="";
            self.root.label_anger.text ="";
        else:            
            self.root.label_last_result.text = MenuScreen.TXT_LAST_CONV_RES
            self.root.label_conversation_txt.text = GUI_EventsManager.conversation_text_recognized.text
            self.root.label_disgust.text = str(GUI_EventsManager.conversation_tone_result_disgust.text)
            self.root.label_joy.text =str(GUI_EventsManager.conversation_tone_result_joy.text)
            self.root.label_fear.text =str(GUI_EventsManager.conversation_tone_result_fear.text)
            self.root.label_sadness.text =str(GUI_EventsManager.conversation_tone_result_sadness.text)
            self.root.label_anger.text =str(GUI_EventsManager.conversation_tone_result_anger.text)
            
            last_tone = GUI_EventsManager.conversation_tone_result.text
            
            yellowStart = "[color=ffff00]"
            yellowEnd = "[/color]"
#              
            if last_tone == 'fear':
                self.root.label_fear.text = yellowStart + self.root.label_fear.text + yellowEnd
            elif last_tone == 'joy':
                self.root.label_joy.text = yellowStart + self.root.label_joy.text + yellowEnd
            elif last_tone == 'disgust':
                self.root.label_disgust.text = yellowStart + self.root.label_disgust.text + yellowEnd
            elif last_tone == 'sadness':
                self.root.label_sadness.text = yellowStart + self.root.label_sadness.text + yellowEnd
            elif last_tone == 'anger':
                self.root.label_anger.text = yellowStart + self.root.label_anger.text + yellowEnd

        
#        GUI_EventsManager.conversation_text_recognized.text = "I more more more called your office several times today and nobody was able to answer. This is damaging your reputations and I request to terminate my contract immediatelly. This is unacceptable and I am very disaposos Blaalalal bllalla lblblbls lkjsfdlkjsfdl. I called your office several times today and nobody was able to answer. This is damaging your reputations and I request to terminate my contract immediatelly. This is unacceptable and I am very disaposos Blaalalal bllalla lblblbls lkjsfdlkjsfdl."
 #       print len(GUI_EventsManager.conversation_text_recognized.text)
#         if len(GUI_EventsManager.conversation_text_recognized.text) > 180:
#             self.root.label_conversation_txt.font_size = RESULT_FONT_SIZE
#         if len(GUI_EventsManager.conversation_text_recognized.text) > 280:
#             self.root.label_conversation_txt.font_size = RESULT_FONT_SIZE_2
#         if len(GUI_EventsManager.conversation_text_recognized.text) > 500:
#             self.root.label_conversation_txt.font_size = RESULT_FONT_SIZE_3
#         
#         if len(GUI_EventsManager.conversation_text_recognized.text) < 180:
#             self.root.label_conversation_txt.font_size = FONT_SIZE
#                 
        
#         tone_res = "Disgust - 200% /t Joy: 0% /n Anger - 0% Fear: 0% /t Sadness - 0%"
#         
#         self.root.label_last_conversation_results.text = tone_res
        
        
        
#         self.
        
#         self.root.infoBox.hello_lable.text = str(GUI_EventsManager.gui_error_event.text)
        

if __name__ == '__main__':
    MainApp().run()