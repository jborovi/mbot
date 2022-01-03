'''
Created on Oct 20, 2016

@author: user
'''
from robot.api.net.NetCom import NetCom
from robot.api import Constants
import sys



if __name__ == '__main__':
    usage = 'usage= sudo python CreateWavFromText \"<Some text in quotes>\" <name of the file>'
    
    print usage
    
    try:
        text = sys.argv[1]
        print text
        
    except Exception, e:
        print 'Text to transform not specified' 
        sys.exit(1)
    try:
        filename = sys.argv[2]
    except Exception, e:
        print 'wav file name not specified'
        sys.exit(1)

    watson = NetCom()
    full_path = Constants.PRESENTATION_WAVS+filename
    try:
        watson.text_to_speech(text, full_path)
        print 'Wav file saved to '+full_path
    except Exception, e:
        print e
    