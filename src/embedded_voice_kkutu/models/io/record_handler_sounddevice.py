import sounddevice as sd
from math import sqrt
import time
import os
import numpy as np
from array import array
from collections import deque

os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["ALSA_CARD"] = "default"

is_adjust_mode = bool("ADJUST_MODE" in os.environ and os.environ["ADJUST_MODE"])


class RecordHandler:
    CHUNK = 1024
    CHANNELS = 1
    RATE = 16000
    SILENCE_THRESHOLD = 0.01
    SILENCE_CHUNKS = 5
    INITIAL_SILENCE_DURATION = 5
    RECORD_PREVIOUS_TEMP_TIME = 0.5

    def __init__(self):
        self.frames = []
        self.previous_frames = deque(maxlen=int(self.RATE * self.RECORD_PREVIOUS_TEMP_TIME))
        self.silent_chunks = 0
        self.is_speaking = False
        self.initial_silence_start = None
        self.recording = False

        # print('RecordHandler initialized with sounddevice')

    def audio_callback(self, indata, frames, _time, status):
        if status:
            print(f'Error: {status}')
            
        audio_data = indata[:, 0]
        rms = self.calculate_rms(audio_data)

        if not self.is_speaking:
            self.previous_frames.extend(audio_data)
            if time.time() - self.initial_silence_start > self.INITIAL_SILENCE_DURATION:
                self.recording = False
                raise sd.CallbackStop()
            if rms > self.SILENCE_THRESHOLD:
                self.is_speaking = True
                self.frames.extend(self.previous_frames)
                self.frames.extend(audio_data)
        else:
            if rms > self.SILENCE_THRESHOLD:
                self.silent_chunks = 0
                self.frames.extend(audio_data)
            else:
                self.silent_chunks += 1
                if self.silent_chunks > self.SILENCE_CHUNKS:
                    self.recording = False
                    raise sd.CallbackStop()
                self.frames.extend(audio_data)

    def record_until_silence(self):
        self.frames = []
        self.previous_frames.clear()
        self.silent_chunks = 0
        self.is_speaking = False
        self.initial_silence_start = time.time()
        self.recording = True

        with sd.InputStream(
            channels=self.CHANNELS,
            samplerate=self.RATE,
            blocksize=self.CHUNK,
            callback=self.audio_callback
        ):
            while self.recording:
                sd.sleep(100)

        return np.array(self.frames, dtype=np.float32)

    def calculate_rms(self, data):
        if len(data) == 0:
            return 0
        return np.sqrt(np.mean(np.square(data)))

if __name__ == "__main__":
    record_handler = RecordHandler()
    frames = record_handler.record_until_silence()
    print(frames)
