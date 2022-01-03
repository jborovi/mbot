import sys
sys.path.append('/home/honza/robot/src')
from robot.api.Helpers import Helpers
from robot.api.sound.SoundMgr import SoundMgr
from robot.api.hw.GPIO_controll import GPIO_controll
from robot.api.Constants import GPIO_button_pin
from robot.api import Constants
import time
from speech_recognition import UnknownValueError
from robot.api.hw.adruinoConnect import AdruionConnect


#turns on/off the sensor
SENSOR_ON = True
    
#turns on/off the iot
IOT_ON = True
#turns on/off the emotions
EMOTION_OUTPUT_ON = False

# BUTTON = True


if __name__ == '__main__':
    from robot.api.net.NetCom import NetCom
    from robot.api.hw.RangeSensor import RangeSensor
    from robot.api.iot.iotClient import IOTClient
    
    buttonControl = GPIO_controll(Constants.GPIO_button_pin)

 #   buttonControl.checkBtn()
#    exit()
#     lightControll = GPIO_controll(GPIO_light_pin)
    
    netcom = NetCom()
    soundMgr = SoundMgr(buttonControl)
    
    
    if EMOTION_OUTPUT_ON:
        adruino = AdruionConnect('/dev/ttyACM0', 9600)
    
    if SENSOR_ON:
        rangeSensor = RangeSensor()
    
    if IOT_ON:
        iotClient = IOTClient()
        
        #cfg file to IOT platform
        iotClient.connect('/home/honza/robot/cfg/device.cfg')
        
        #iot message send, should be vissible in bluemix iot robot iot, device coolrobot 
        iotClient.send_json_msg({'status':'robot connected'})
    
    
    #contant trigering movement detection, or speech detection
    isMovement = False
    
    conversationTime = 0
    conversationStarted = 0
    
    
    tellAjoke = False
    
    repeatSpeech = False
    
    #based on count of not understand (silence) the detection of movement or speech is trigered
    didNotUnderstandCount = 0
    
    greetingsCount = 0
    
    #array with greetings, its iterating in loop
    greetings = [Constants.WAW_GREETING]
    
    converstationTryCound = 0
    
    
    while True:
        if EMOTION_OUTPUT_ON:
            try:
                adruino.write_emotion('sleep')
                
            except Exception,e:
                print e
                print 'Exception in set emotion adruino.'

        try:
#             block with movement detection logic, if movement is detected, speech detection is trigered
            if SENSOR_ON:
                isMovement = rangeSensor.getMovement()
                if isMovement:
                    if EMOTION_OUTPUT_ON:
                        try:
                            adruino.write_emotion('joy')
                            
                        except Exception,e:
                            print 'Exception in set emotion adruino'
                    
                    if IOT_ON:
                        iotClient.send_json_msg({'status':'motion detected'})
            else:
                isMovement = True
        except Exception,e:
            print 'Exception in rangeSensor'
            print e
            
        #if movement was detected, speech detection is trigered, movement detection is disabled until speech detection finishes
        if isMovement:
            try:
                conversationStarted = time.time()
#                 buttonControl.checkBtn()
#                 lightControll.change_status(buttonControl.is_on())
                if IOT_ON:
                    iotClient.send_json_msg({'status':'start conversation'})
                
#                 netcom.text_to_speech(greetings[0], Constants.WAW_PATH)
#                 else:
#                     if converstationTryCound > 3:
#                         converstationTryCound = 0
#                     netcom.text_to_speech(greetings[greetingsCount], Constants.WAW_PRESS_BUTTON)
                #current wav played    
                soundMgr.play_wav(Constants.WAW_GREETING_F)
                recorded = soundMgr.record_to_file(Constants.WAW_RECORD_INPUT)
#                 lightControll.change_status(buttonControl.is_on())
                if not recorded:
                    continue
                else:
                #sound recognition started
#                     netcom.text_to_speech(Constants.MSG_CONTINUE_CONF, Constants.WAW_PATH)    
                    soundMgr.play_wav(Constants.MSG_CONTINUE_CONF_F)
                    
                    recognized_sound  = netcom.recognize(Constants.WAW_RECORD_INPUT)
                    
                    #get the emotion from the recognized text
                    netcom.analyzed_emotion = netcom.analyze(recognized_sound)
                    if IOT_ON:
                        iotClient.send_json_msg({'status':'emotion detected'})
                        iotClient.send_json_msg({'emotion':netcom.analyzed_emotion})
                        
                    
                    if EMOTION_OUTPUT_ON:
                        try:
                            #triger emotion output in adruiion
                            adruino.write_emotion(netcom.analyzed_emotion)                        
                        except Exception,e:
                            print 'Exception in set emotion adruino'
                        
                        #generate emotion wav
                    netcom.set_reply_wav(netcom.analyzed_emotion)
                    #play emotion wav                
#                     netcom.text_to_speech(netcom.emotion_wav, Constants.WAW_PATH)    
                    soundMgr.play_wav(netcom.emotion_wav)
                
            except UnknownValueError, uve:
                didNotUnderstandCount += 1
                print 'Sensor did not understand, or nobody spoke'
                 
                if EMOTION_OUTPUT_ON:
                    try:
                        adruino.write_emotion('fear')
                    except Exception,e:
                        print 'Exception in set emotion adruino'
                     
#                 netcom.text_to_speech(Constants.MSG_DONT_UNDERSTAND, Constants.WAW_PATH)    
                soundMgr.play_wav(Constants.WAW_DONT_UNDERSTAND)
            except Exception, e:
                print e
                
                didNotUnderstandCount += 1
                print 'Exception in speech'
            
                 
            if didNotUnderstandCount > 3:
                #in this block the speech recognition part is disabled nad movement detection is trigered
                didNotUnderstandCount = 0
                isMovement = False
#                 
            

