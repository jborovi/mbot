'''
Created on Oct 20, 2016

@author: user
'''
from robot.api.hw.adruinoConnect import AdruionConnect
from robot.api.sound import SoundMgr2
from robot.api.sound.SoundMgr2 import Recorder
from robot.api import Constants

class DisplayEmotionAndPlayWav(object):
     
    '''
    classdocs
    '''
    def __init__(self):
        self.adruino = AdruionConnect('/dev/ttyACM0', 9600)
        self.soundmgr = Recorder()
        
        
    
    def display_emo(self, emo):
        self.adruino.write_emotion(emo)
#         self.adruino.close()
        
    def play_wav(self, wav_path):
        self.soundmgr.play_wav(wav_path, use_default_path=False)


if __name__ == '__main__':
    print "emotions list"
    print 'neutral, anger, disgust, sadness, fear, scared, joy, sleep, wakeup'
    usage =  'usage = sudo python DisplayEmotionAndPlayWav.py <emotion> <wav_path>'
    import sys
    
    play_wav = False
    
    try:
        emotion = sys.argv[1]
        print emotion
    except Exception, e:
        print usage 
        sys.exit(1)
    try:
        filename = sys.argv[2]
        play_wav = True
    except Exception, e:
        print 'wav file not specified, will only display emotion'
    
    mbot = DisplayEmotionAndPlayWav()
    print '111'
    import time
#     time.sleep(5)

    print '222'
    print '333'
    if play_wav:
        wav_path = Constants.PRESENTATION_WAVS  + filename
        print wav_path
        mbot.play_wav(wav_path)
        print '444'