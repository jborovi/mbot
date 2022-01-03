import pyaudio
import wave
import threading


class TestSound(object):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 60  # 1 minute max audio file
    WAVE_OUTPUT_FILENAME = "file.wav"

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                rate=self.RATE, input=True,
                                frames_per_buffer=self.CHUNK)
        self.frames = []
    
    def recording(self):
#         print("Recording...")
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
    
    def stop_recording(self):
#         print 'stop recording'
        stop = input("Press Enter to stop recording.")
        if stop == "":
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

if __name__ == '__main__':
    #just for testing ...
    test = TestSound()
    t1 = threading.Thread(target=test.recording(), args=(), daemon=True)
    t2 = threading.Thread(target=test.stop_recording(), args=(), daemon=True)
    
    t1.start()
    t2.start()
#     recording()