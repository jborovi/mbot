'''
Created on Sep 29, 2016

@author: user
'''
import sys
import signal
from datetime import datetime
sys.path.append('/home/mbot/mbotProject/src')
from robot.api.controll.ThreadControll import ThreadControll
import logging
from robot.api.controll.EventsManager import EventsManager
import threading
from robot.api.hw.RangeSensor import RangeSensor
import time
from robot.api.controll.DemoModeController import DemoModeController
from robot.api.hw.adruinoConnect import AdruionConnect
from robot.api.sound.SoundMgr2 import Recorder
from robot.api.controll.ConversationFlowController import ConversationFlowController
from robot.api.controll.ButtonController import ButtonController
from robot.api import Constants
from robot.api.controll.SoundRecordController import SoundRecordController
from robot.api.kivygui.UserInputScreen import MainApp
from robot.api.controll.GUI_EventsManager import GUI_EventsManager

class MainController(ThreadControll):
    
    #Main Controller Method, from here all threads are initialized*
    
    
    #turns on/off the sensor
    SENSOR_ON = False


    def wait_for_event(self, e):
        #Empty method doing nothing, not called#
        super(MainController, self).wait_for_event(e)
        
        if EventsManager.startEvent.isSet():
            self.init_robot()
#         if EventsManager.sleepMode.isSet():
#             self.sleepModeThread.start()

#             print 'sleepMode'
    
    def wait_for_event_timeout(self, e, t):
        ##initializes all threads from main thread and sets neutral and sleep emotions#
        while not e.isSet():
#             print 'MAIN thread runing'
            event_is_set = e.wait(t)

            if EventsManager.startEvent.isSet():
                self.init_robot()
            if EventsManager.neutralMode.isSet():
                self.adruino.write_emotion("neutral")
            if EventsManager.sleepMode.isSet():
                self.adruino.write_emotion("sleep")

#             GUI_EventsManager.conversation_tone_result =
    
#         print 'MAIN thread dead'
        sys.exit()


        
    def init_robot(self):        
        #robot initialization
        print 'MBOT:'+str(datetime.now()) + str("Robot started ...")
        self.adruino = AdruionConnect('/dev/ttyACM0', 9600)
        self.sound_mgr = Recorder(channels=2)
        try:
            GUI_EventsManager.ip_address_event.text= self.get_ip()
        except Exception, e:
            GUI_EventsManager.ip_address_event.text = 'No IP'
            print 'MBOT:'+str(datetime.now()) + str("Could not get IP")
        
        self.init_threads()
        EventsManager.startEvent.clear()
        EventsManager.neutralMode.set()
        
    def init_threads(self):
        #threads initialization
        self.range_sensor_input_thread = RangeSensor()
        self.demo_mode_output_thread = DemoModeController(self.adruino, self.sound_mgr, 5)
        self.conversationFlowController = ConversationFlowController(self.sound_mgr, self.adruino)
        self.button_input_controller = ButtonController(Constants.GPIO_button_pin)
        self.sound_record_input_controller = SoundRecordController(self.sound_mgr)
        
        
        #checking input from the range sensor every 0.5 second and manipulating the states based on the event logic
        self.rangeSensorThread = threading.Thread(name='rangeSensorThread', 
                      target=self.range_sensor_input_thread.wait_for_event_timeout,
                      args=(EventsManager.endRobot,0.5))
        self.rangeSensorThread.daemon = True
        
        #displays demomode states on robots face untile demomode event is clear
        self.demoModeThread = threading.Thread(name='demoModeThread', 
                      target=self.demo_mode_output_thread.wait_for_event_timeout,
                      args=(EventsManager.endRobot,1))
        self.demoModeThread.daemon = True
        
        #conversation logic thread
        self.conversationFlowThread = threading.Thread(name='conversationFlowThread', 
                      target=self.conversationFlowController.wait_for_event_timeout,
                      args=(EventsManager.endRobot,1))
        self.conversationFlowThread.daemon=True
        #big blue button events thread
        self.button_input_thread = threading.Thread(name='buttonInputThread', 
                      target=self.button_input_controller.wait_for_event_timeout,
                      args=(EventsManager.endRobot,0.1))
        self.button_input_thread.daemon=True
        #sound recording thread
        self.sound_record_input_thread = threading.Thread(name='soundInputRecordThread', 
                      target=self.sound_record_input_controller.wait_for_event_timeout,
                      args=(EventsManager.endRobot,0.1))
        self.sound_record_input_thread.daemon=True
#         
#         self.gui_thread = threading.Thread(name='userInterfaceThread', 
#                       target=self.gui_controller.wait_for_event_timeout,
#                       args=(EventsManager.endRobot,0.5))
#         self.gui_thread.daemon=True

        
        self.rangeSensorThread.start()
        self.demoModeThread.start()
        self.conversationFlowThread.start()
        self.button_input_thread.start()
        self.sound_record_input_thread.start()
        
        
        
    def get_ip(self):        
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
        local_ip_address = s.getsockname()[0]
        return local_ip_address
#         self.gui_thread.start()


def sighandler(signum, frame):
    print 'signal handler called with signal: %s ' % signum
    EventsManager.endRobot.set()


def main(argv=None):
    signal.signal(signal.SIGTERM, sighandler) # so we can handle kill gracefully
    signal.signal(signal.SIGINT, sighandler) # so we can handle ctrl-c
    try:

        main = MainController()
        mainThread = threading.Thread(name='mainThread', 
                          target=main.wait_for_event_timeout,
                          args=(EventsManager.endRobot,1))
        
        mainThread.start()
        EventsManager.startEvent.set()
        EventsManager.say_hello.set()
        MainApp().run()
    except Exception, reason:
        print 'MBOT:'+str(datetime.now()) + str(reason)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
#     def sighandler( signum, frame):
#         print 'signal handler called with signal: %s ' % signum
#         EventsManager.endRobot.set()
#         global shutdown_flag
#         shutdown_flag = True
    
    
    #init audio
#     import os
#     os.system('sudo audio_Reset_paths.sh')
#     print 'init record'
#     os.system('sudo audio_Record_from_lineIn_Micbias.sh')
#     print "init playback"
#     os.system('sudo audio_Playback_to_Lineout.sh')
#     print 'init finished'
#     
# #     signal.signal(signal.SIGTERM, sighandler) # so we can handle kill gracefully
# #     signal.signal(signal.SIGINT, sighandler) # so we can handle ctrl-c
#     
#     main = MainController()
#     mainThread = threading.Thread(name='mainThread', 
#                       target=main.wait_for_event_timeout,
#                       args=(EventsManager.endRobot,1))
#     
#     mainThread.start()
#     EventsManager.startEvent.set()
#     EventsManager.say_hello.set()
#     MainApp().run()
    