'''
Created on Apr 26, 2016

@author: user
'''
import pyaudio
import wave
from array import array
from struct import pack
from sys import byteorder
from robot.api.hw.GPIO_controll import GPIO_controll
from robot.api import Constants
import copy
class SoundMgr(object):
#     '''
#     classdocs
#     '''
    
    def __init__(self, recordController):
#         if isinstance(recordController, GPIO_controll):
        self.record_controller = recordController
#         if isinstance(recordController, GPIO_controll):            
#         else:
#             raise Exception('invalid parameter in SoundMgr init')
    
    
    def play_wav(self, wav_filename):
        '''
        Play (on the attached system sound device) the WAV file
        named wav_filename.
        '''
        import os
        os.system('aplay '+Constants.SOUNDS_FOLDER+wav_filename)
#         
# #Instead of adding silence at start and end of recording (values=0) I add the original audio . This makes audio sound more natural as volume is >0. See trim()
# #I also fixed issue with the previous code - accumulated silence counter needs to be cleared once recording is resumed.

    
    THRESHOLD = 500  # audio levels not normalised.
    CHUNK_SIZE = 512
    SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
    FORMAT = pyaudio.paInt16
    FRAME_MAX_VALUE = 2 ** 15 - 1
    NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
    RATE = 44100
    CHANNELS = 1
    TRIM_APPEND = RATE / 4
    
    def is_silent(self, data_chunk):
        """Returns 'True' if below the 'silent' threshold"""
#         self.light_controller.change_status(self.record_controller.is_on())
#         print self.record_controller.is_on()
        return not self.record_controller.is_on()
#         return max(data_chunk) < self.THRESHOLD
    
    def normalize(self,data_all):
        """Amplify the volume out to max -1dB"""
        # MAXIMUM = 16384
        normalize_factor = (float(self.NORMALIZE_MINUS_ONE_dB * self.FRAME_MAX_VALUE)
                            / max(abs(i) for i in data_all))
    
        r = array('h')
        for i in data_all:
            r.append(int(i * normalize_factor))
        return r
    
    def trim(self,data_all):
        _from = 0
        _to = len(data_all) - 1
        for i, b in enumerate(data_all):
            if abs(b) > self.THRESHOLD:
                _from = max(0, i - self.TRIM_APPEND)
                break
    
        for i, b in enumerate(reversed(data_all)):
            if abs(b) > self.THRESHOLD:
                _to = min(len(data_all) - 1, len(data_all) - 1 - i + self.TRIM_APPEND)
                break
    
        return copy.deepcopy(data_all[_from:(_to + 1)])
    
    def record(self):
        """Record a word or words from the microphone and 
        return the data as an array of signed shorts."""
    
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, output=True, frames_per_buffer=self.CHUNK_SIZE)
    
        silent_chunks = 0
        audio_started = False
        data_all = array('h')
    
        while True:
            # little endian, signed short
            data_chunk = array('h', stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                data_chunk.byteswap()
            data_all.extend(data_chunk)
    
            silent = self.is_silent(data_chunk)
    
            if audio_started:
                if silent:
                    silent_chunks += 1
                    if silent_chunks > self.SILENT_CHUNKS:
                        break
                else: 
                    silent_chunks = 0
            elif not silent:
                audio_started = True              
    
        sample_width = p.get_sample_size(self.FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()
    
        data_all = self.trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
        data_all = self.normalize(data_all)
        return sample_width, data_all
    
    def record_to_file(self,path):
        import time
        
        start = time.time()
        
        self.record_controller.setDebugFalseOnFor(15)
        
        while True:
            if self.record_controller.is_on():
#                 print "Button pressed"
#                 self.light_controller.change_status(self.record_controller.is_on())
                break
            else:
                if time.time() - start > Constants.BUTTON_WAIT_RECORD:
                    print 'Recording waited for 5 seconds for button'
                    return False
                
        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = self.record()
        data = pack('<' + ('h' * len(data)), *data)
    
        wave_file = wave.open(path, 'wb')
        wave_file.setnchannels(self.CHANNELS)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(self.RATE)
        wave_file.writeframes(data)
        wave_file.close()
        return True

# if __name__ == '__main__':
#     print("Wait in silence to begin recording; wait in silence to terminate")
#     record_to_file('/home/honza/_tmp/demo.wav')
#     print("done - result written to demo.wav")


    
