# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
#from watson_developer_cloud.tone_analyzer_v3_beta import ToneAnalyzerV3Beta
from watson_developer_cloud import ToneAnalyzerV3
import json
from watson_developer_cloud.text_to_speech_v1 import TextToSpeechV1
from os.path import join, dirname

import pyaudio
import wave
import sys
from robot.api import Constants
from robot.api.sound.SoundMgr import SoundMgr
from robot.api.common.common import Common


    


class NetCom():
    
    emotion_wav = None
    analyzed_emotion = None
    
    def __init__(self):
        pass

    def set_reply_wav(self, emotion):
        if(emotion == 'anger'):
            self.emotion_wav = Constants.MSG_ANGER_F
        elif (emotion == 'disgust'):
            self.emotion_wav = Constants.MSG_DISTUST_F
        elif (emotion == 'sadness'):
            self.emotion_wav = Constants.MSG_NEGATIVE_1_F
        elif(emotion == 'scared' or emotion == 'fear'):
            self.emotion_wav = Constants.MSG_SCARED_1_F
        elif(emotion == 'joy'):
            self.emotion_wav = Constants.MSG_POSITIVE_1_F
        else:
            self.emotion_wav = Constants.MSG_DONT_UNDERSTAND_F
    
    def get_tone(self,analyze):
        last_score = 0
        last_tone = None
         
        document_tone = analyze['document_tone']
        tone_categories = document_tone['tone_categories']
        for category in tone_categories:
            if category['category_id']!='emotion_tone':
                continue
            else:
                tones = category['tones']
                for tone in tones:

                    this_tone = tone['tone_id']
                    this_score = tone['score']

                    if this_tone == 'anger':
                        Common.tty_print(text=str(this_tone) +" "+ str(this_score*100)+"%", color='red')
                    if this_tone == 'disgust':
                        Common.tty_print(text=str(this_tone) +" "+ str(this_score*100)+"%", color='yellow')
                    if this_tone == 'fear':
                        Common.tty_print(text=str(this_tone) +" "+ str(this_score*100)+"%", color='white')
                    if this_tone == 'sadness':
                        Common.tty_print(text=str(this_tone) +" "+ str(this_score*100)+"%", color='cyan')
                    if this_tone == 'joy':
                        Common.tty_print(text=str(this_tone) +" "+ str(this_score*100)+"%", color='magenta')

                    if this_score >= last_score:
                        last_tone = this_tone
                        last_score = this_score

        Common.tty_print(text='The tone is: '+str(last_tone),color='green')
        return last_tone
     
     
    def recognize(self, wav_path):
        # obtain audio from the microphone
        r = sr.Recognizer()

#         with sr.Microphone() as source:
#	    r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
#             print("Say something!")
#             audio = r.listen(source)
        Common.tty_print(text="Sending recorded sound for analyze ...",newDialog=True) 
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source) # read the entire audio file
        IBM_USERNAME = "4b344931-9254-4738-af5d-b273725b8011" # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        IBM_PASSWORD = "smCaRqINM17g" # IBM Speech to Text passwords are mixed-case alphanumeric strings
        # write audio to a WAV file
#         with open("/home/honza/_tmp/microphone-results.wav", "wb") as f:
#             f.write(audio.get_wav_data())
        try:
            analyze_text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
            Common.tty_print("IBM Speech to Text thinks you said: \"" + str(analyze_text)+"\"")
            return analyze_text
        except sr.UnknownValueError as e:        
            Common.tty_print("IBM Speech to Text could not understand audio")
            raise e
        except sr.RequestError as e:
            Common.tty_print("Could not request results from IBM Speech to Text service; {0}".format(e))
            raise e
            
    def analyze(self,txt):
        Common.tty_print('Analyzing emotion ...')
        tone_analyzer = ToneAnalyzerV3(
            username='acc971eb-33dd-45d9-b4d7-8f0b6f3584f8',
            password='3qHV7kKqcKk8',
            version='2016-02-11')
        analyze_res = tone_analyzer.tone(text=txt)
        return self.get_tone(analyze_res)
     
    def text_to_speech(self, text, wav_path):
        text_to_speech = TextToSpeechV1(
                username="5f02f1bc-56b4-4bdf-ac10-134a94a1fd5c",
                 password="zUl8piqTscEN")
              
#         print(json.dumps(text_to_speech.voices(), indent=2))
             
        with open(join(dirname(__file__), wav_path), 'wb') as audio_file:
            audio_file.write(text_to_speech.synthesize(text=text, accept="audio/wav"))
     
