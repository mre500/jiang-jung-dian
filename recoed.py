import pyaudio
import time
import threading
import wave

class Recorder():
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
    def start(self):
        threading._start_new_thread(self.__recording, ())
    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while(self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
    def stop(self):
        self._running = False
    def save(self, filename):
        p = pyaudio.PyAudio()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()

def recording_end(language = "", speaker_name = "", action = ""):
    if action == "enroll":
        filename = "./data/enroll/wav/" + speaker_name + "_" + language + ".wav"
    if action == "recog":
        filename = "./data/recog/meeting" + "_" + time.strftime("%Y-%m%d-%H%M%S", time.localtime()) + ".wav"
    rec.stop()
    rec.save(filename = filename)