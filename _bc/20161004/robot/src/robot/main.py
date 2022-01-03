import sys
sys.path.append('/home/honza/robot/src')
from robot.api.common.common import Common
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
EMOTION_OUTPUT_ON = True

# BUTTON = True


if __name__ == '__main__':
    from robot.api.net.NetCom import NetCom
    from robot.api.hw.RangeSensor import RangeSensor
    from robot.api.iot.iotClient import IOTClient
    
    buttonControl = GPIO_controll(Constants.GPIO_button_pin)

 #   buttonControl.checkBtn()
#    exit()
#     lightControll = GPIO_controll(GPIO_light_pin)

    movement_detection_started = None
    
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
    
    is_demo_mode = False
    
    demo_last_triggered = None
    
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
#                 print e
                Common.tty_print('Exception in set emotion adruino.')

        try:
#             block with movement detection logic, if movement is detected, speech detection is trigered
            if SENSOR_ON:
                
                demo_triger = rangeSensor.get_demo_mode_trigger()
#                 print 'demo triger'
                if demo_triger:
                    is_demo_mode = not is_demo_mode
                    if is_demo_mode:
                        demo_mode_count = 0
                        demo_last_triggered = time.time()
                    
#                 print 'is demo'
#                 print is_demo_mode
                
                if is_demo_mode:
                    
                    if demo_mode_count == 0 or ((time.time() - demo_last_triggered) > Constants.ROBOT_DEMO_MODE_PERIOD):
                        demo_last_triggered = time.time()
                        if demo_mode_count == 0:
                            soundMgr.play_wav(Constants.WAV_DEMO_MODE_F)

                        demo_mode_count += 1
                        adruino.write_emotion('wakeup')
                        time.sleep(10)
                        if rangeSensor.get_demo_mode_trigger():
                            is_demo_mode = False
                            time.sleep(10)
                            continue
                        adruino.write_emotion('neutral')
                        if rangeSensor.get_demo_mode_trigger():
                            is_demo_mode = False
                            time.sleep(10)
                            continue
                        time.sleep(10)
                        if rangeSensor.get_demo_mode_trigger():
                            is_demo_mode = False
                            time.sleep(10)
                            continue
                        adruino.write_emotion('anger')
                        if rangeSensor.get_demo_mode_trigger():
                            is_demo_mode = False
                            time.sleep(10)
                            continue
                        time.sleep(10)
                        adruino.write_emotion('disgust')
                        if rangeSensor.get_demo_mode_trigger():
                            is_demo_mode = False
                            time.sleep(10)
                            continue
                        time.sleep(10)
                        adruino.write_emotion('fear')
                        if rangeSensor.get_demo_mode_trigger():
                            is_demo_mode = False
                            time.sleep(10)
                            continue
                        time.sleep(10)
                        adruino.write_emotion('joy')
                        if rangeSensor.get_demo_mode_trigger():
                            is_demo_mode = False
                            time.sleep(10)
                            continue         
                        time.sleep(10)
                        adruino.write_emotion('sleep')
                        if rangeSensor.get_demo_mode_trigger():
                            is_demo_mode = False
                            time.sleep(10)
                            continue
                        time.sleep(10)
                    else:
                        continue
                else:
                    demo_last_triggered = None
                
                isMovement = rangeSensor.getMovement()
                if isMovement:
                    if EMOTION_OUTPUT_ON:
                        try:
                            adruino.write_emotion('wakeup')    
                        except Exception,e:
                            Common.tty_print('Exception in set emotion adruino')
                        
                    if IOT_ON:
                        iotClient.send_json_msg({'status':'motion detected'})
            else:
                isMovement = True
        except Exception,e:
            Common.tty_print('Exception in rangeSensor')
#             print e
            
        #if movement was detected, speech detection is trigered, movement detection is disabled until speech detection finishes
        if isMovement:
            try:
                conversationStarted = time.time()
                if IOT_ON:
                   iotClient.send_json_msg({'status':'start conversation'})
                
                #current wav played    
                soundMgr.play_wav(Constants.WAW_GREETING_F)
                recorded = soundMgr.record_to_file(Constants.WAW_RECORD_INPUT)
                if not recorded:
                    continue
                else:    
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
                            Common.tty_print('Exception in set emotion adruino')
                        
                        #generate emotion wav
                    netcom.set_reply_wav(netcom.analyzed_emotion)    
                    soundMgr.play_wav(netcom.emotion_wav)
                    time.sleep(10)
                    adruino.write_emotion('sleep')
                    movement_detection_started = time.time()
                    time.sleep(20)
                
            except UnknownValueError, uve:
                didNotUnderstandCount += 1
                Common.tty_print('Sensor did not understand, or nobody spoke')
                 
                if EMOTION_OUTPUT_ON:
                    try:
                        adruino.write_emotion('fear')
                    except Exception,e:
                        Common.tty_print('Exception in set emotion adruino')
                     
#                 netcom.text_to_speech(Constants.MSG_DONT_UNDERSTAND, Constants.WAW_PATH)    
                soundMgr.play_wav(Constants.MSG_DONT_UNDERSTAND_F)
                time.sleep(10)
                adruino.write_emotion('sleep')
                movement_detection_started = time.time()
                time.sleep(20)
            except Exception, e:
#                 print e
                
                didNotUnderstandCount +=1
                Common.tty_print('Exception in speech')
            
                 
            if didNotUnderstandCount > 3:
                #in this block the speech recognition part is disabled nad movement detection is trigered
                didNotUnderstandCount = 0
                isMovement = False
#                 
            

