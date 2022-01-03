'''recorder.py
Provides WAV recording functionality via two approaches:
Blocking mode (record for a set duration):
>>> rec = Recorder(channels=2)
>>> with rec.open('blocking.wav', 'wb') as recfile:
...     recfile.record(duration=5.0)
Non-blocking mode (start and stop recording):
>>> rec = Recorder(channels=2)
>>> with rec.open('nonblocking.wav', 'wb') as recfile2:
...     recfile2.start_recording()
...     time.sleep(5.0)
...     recfile2.stop_recording()
'''
import pyaudio
import wave
import time
from robot.api import Constants
from robot.api.controll.EventsManager import EventsManager
from datetime import datetime

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=2, rate=44100, frames_per_buffer=2048):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.recording = False

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)
        
        
    def record_to_file(self, waw_path):
        if self.recording:
            return
        with self.open(waw_path, 'wb') as recfile2:
            recfile2.start_recording()            
            while EventsManager.button_is_pressed.isSet():
                time.sleep(0.1)
            self.recording = False
            recfile2.stop_recording()
        
    def play_wav(self, wav_filename, wait_till_finish=True, use_default_path = True):
        '''
        Play (on the attached system sound device) the WAV file
        named wav_filename.
        '''
        
        if use_default_path:
            sounds_path = Constants.SOUNDS_FOLDER
        else:
            sounds_path = ''
        
        import os
        if wait_till_finish:
            os.system('aplay '+sounds_path+wav_filename)#+' &')
        else:
            os.system('aplay '+sounds_path+wav_filename+' &')



class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
#         stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, output=True, frames_per_buffer=self.CHUNK_SIZE)
        
        try:
            self._stream = self._pa.open(format=pyaudio.paInt16,
                                            channels=self.channels,
                                            rate=self.rate,
                                            input=True,
                                            frames_per_buffer=self.frames_per_buffer,
                                            stream_callback=self.get_callback())
        except Exception, e:
            print 'MBOT:'+str(datetime.now()) + "exception in start_recording"
            print 'MBOT:'+str(datetime.now()) + str(e)
        self._stream.start_stream()
        self.recording = True
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        self.recording = False
        EventsManager.trigger_get_emotion_results()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)            
            return in_data, pyaudio.paContinue
        return callback

    def close(self):
        try: 
            self._stream.close()
        except Exception, e:
            print 'MBOT:'+str(datetime.now()) + "exception in SoundMgr2 close"
            print 'MBOT:'+str(datetime.now()) + str(e)
        try:
            self._pa.terminate()
        except Exception, e:
            print 'MBOT:'+str(datetime.now()) + "exception in SoundMgr2 close"
            print 'MBOT:'+str(datetime.now()) + str(e)
        try:
            self.wavefile.close()
        except Exception, e:
            print 'MBOT:'+str(datetime.now()) + "exception in SoundMgr2 close"
            print 'MBOT:'+str(datetime.now()) + str(e)

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile
    
if __name__ == '__main__':
    rec = Recorder(channels=2)
#     rec.record_to_file('c:\\nonblocking.wav')
#     rec.record_to_file('/home/honza/_tmp/input.wav')
#     with rec.open('c:\\nonblocking.wav', 'wb') as recfile2:
    with rec.open('/home/czz82971/input.wav', 'wb') as recfile2:
        recfile2.start_recording()
        time.sleep(10)
        recfile2.stop_recording()
