import sys
sys.path.append('/home/honza/robot/src')
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
    
#     MSG_NEGATIVE_1 = 'Ohh I am sorry. Well It sounds pretty sad to me. How about telling me something more optimistic to cheer me up ?'
# MSG_NEGATIVE_1_F = 'negative1.wav'
# 
# MSG_ANGER = 'Damn it !  This makes me feel angry !'
# MSG_ANGER_F = 'anger.wav'
# 
# MSG_DISGUST = 'Wow, did i hear you correctly ? Because this is disgusting !'
# MSG_DISTUST_F = 'disgust.wav' 
#  
# MSG_SCARED_1 = 'I can sense fear, this makes me feel scared.'
# MSG_SCARED_1_F = 'scared1.wav'
# 
# MSG_POSITIVE_1 = 'This sounds joyful.  Life is good.'
# MSG_POSITIVE_1_F = 'positive1.wav'
#     
# MSG_CONFUSED = 'I am having troubles understanding you. Please talk again or rise a ticket to my programmers as I feel confused.'
# MSG_CONFUSED_F = 'confused.wav'
# 
# MSG_DONT_UNDERSTAND = 'I am having troubles understanding you. Please talk again or rise a ticket to my programmers as I feel confused.'
# MSG_DONT_UNDERSTAND_F = 'dontUnderstand.wav'
# 
# # MSG_WILL_TELL_YOU = 'Just for fun, I will tell you what I understod'
# 
# MSG_CONTINUE_CONF = "Let me consult Watson to analyze the emotion."
# MSG_CONTINUE_CONF_F = 'continueConversation.wav'
# 
# WAW_PATH = "/home/honza/_tmp/output.wav"
# 
# WAW_DONT_UNDERSTAND = '/home/honza/_tmp/dontunderstand.wav'
# 
# WAW_GREETING = 'Hello, please press and hold the red button while you are talking and I will  listen to you.'
# WAW_GREETING_F = 'greeting.wav'

    
    soundMgr = SoundMgr(buttonControl)
    
    
    if EMOTION_OUTPUT_ON:
        adruino = AdruionConnect('/dev/ttyAMA0', 9600)
#         {'neutral':'0', 'anger':'1', 'disgust':'1', 'sadness':'4', 'fear':'2', 'scared':'2', 'scared':'2', 'joy':'3', 'sleep':'5', 'wakeup':'6'}
#         adruino.write_emotion('sleep')
        
    
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
                print e
                print 'Exception in set emotion adruino.'

        try:
#             block with movement detection logic, if movement is detected, speech detection is trigered
            if SENSOR_ON:
                
                demo_triger = rangeSensor.get_demo_mode_trigger()
                print 'demo triger'
                if demo_triger:
                    is_demo_mode = not is_demo_mode
                    if is_demo_mode:
                        demo_mode_count = 0
                        demo_last_triggered = time.time()
                    
                print 'is demo'
                print is_demo_mode
                
                if is_demo_mode:
                    if demo_last_triggered is not None:
                        print '(time.time() - demo_last_triggered) < Constants.ROBOT_DEMO_MODE_PERIOD'
                        print (time.time() - demo_last_triggered) < Constants.ROBOT_DEMO_MODE_PERIOD
                        print (time.time() - demo_last_triggered)
                
                    print "demo_last_triggered"
                    print demo_last_triggered
                    
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
                    time.sleep(10)
                    adruino.write_emotion('sleep')
                    movement_detection_started = time.time()
                    time.sleep(20)
                
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
                time.sleep(10)
                adruino.write_emotion('sleep')
                movement_detection_started = time.time()
                time.sleep(20)
            except Exception, e:
                print e
                
                didNotUnderstandCount += 1
                print 'Exception in speech'
            
                 
            if didNotUnderstandCount > 3:
                #in this block the speech recognition part is disabled nad movement detection is trigered
                didNotUnderstandCount = 0
                isMovement = False
#                 
            

