'''
Created on Apr 26, 2016

@author: user
'''

SOUNDS_FOLDER = '/home/honza/robot/res/sounds/'

MSG_NEGATIVE_1 = 'Ohh I am sorry. Well It sounds pretty sad to me. How about telling me something more optimistic to cheer me up ?'
MSG_NEGATIVE_1_F = 'negative1.wav'

MSG_ANGER = 'Damn it !  This makes me feel angry !'
MSG_ANGER_F = 'anger.wav'

MSG_DISGUST = 'Wow, did i hear you correctly ? Because this is disgusting !'
MSG_DISTUST_F = 'disgust.wav' 
 
MSG_SCARED_1 = 'I can sense fear, this makes me feel scared.'
MSG_SCARED_1_F = 'scared1.wav'

MSG_POSITIVE_1 = 'This sounds joyful.  Life is good.'
MSG_POSITIVE_1_F = 'positive1.wav'
    
MSG_CONFUSED = 'I am having troubles understanding you. Please talk again or rise a ticket to my programmers as I feel confused.'
MSG_CONFUSED_F = 'confused.wav'

MSG_DONT_UNDERSTAND = 'I am having troubles understanding you. Please talk again or rise a ticket to my programmers as I feel confused.'
MSG_DONT_UNDERSTAND_F = 'dontUnderstand.wav'

# MSG_WILL_TELL_YOU = 'Just for fun, I will tell you what I understod'

MSG_CONTINUE_CONF = "Let me consult Watson to analyze the emotion."
MSG_CONTINUE_CONF_F = 'continueConversation.wav'

WAW_PATH = "/home/honza/_tmp/output.wav"

WAW_DONT_UNDERSTAND = '/home/honza/_tmp/dontunderstand.wav'

WAW_GREETING = 'Hello, please press and hold the red button while you are talking and I will  listen to you.'
WAW_GREETING_F = 'greeting.wav'

WAV_DEMO_MODE = 'I am starting demo mode.'
WAV_DEMO_MODE_F = 'demoMode.wav'

# WAW_PRESS_BUTTON = "Please hold the button to start the conversation"

WAW_RECORD_INPUT = "/home/honza/robot/res/sounds/input.wav"


GPIO_button_pin = 2

GPIO_light_pin = 10

BUTTON_WAIT_RECORD = 30

ROBOT_DEMO_MODE_PERIOD = 300
# ROBOT_DEMO_MODE_PERIOD = 120


EVENT_KILL = 1
IOT_CONNECT = 2
IOT_MSG = 3
EVENT_INIT = 4
EVENT_DEMO_MODE = 5
EVENT_NORMAL_MODE = 6
EVENT_WAKE_UP = 7
EVENT_SLEEP = 8
EVENT_NEUTRAL = 9
EVENT_ANGER = 10
EVENT_DISGUST = 11
EVENT_SADNESS = 12
EVENT_FEAR = 13
EVENT_SCARED = 14
EVENT_JOY = 15
EVENT_SLEEP = 16
EVENT_BUTTON_HOLD = 17
EVENT_BUTTON_NOT_HOLD = 18