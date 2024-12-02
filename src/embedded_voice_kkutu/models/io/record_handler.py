import pyaudio
from array import array

class RecordHandler:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    SILENCE_THRESHOLD = 1000
    SILENCE_CHUNKS = 30 

    def __init__(self):
        self.CHUNK = RecordHandler.CHUNK
        self.FORMAT = RecordHandler.FORMAT
        self.CHANNELS = RecordHandler.CHANNELS
        self.RATE = RecordHandler.RATE
        self.SILENCE_THRESHOLD = RecordHandler.SILENCE_THRESHOLD
        self.SILENCE_CHUNKS = RecordHandler.SILENCE_CHUNKS
        
    def record_until_silence(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                       channels=self.CHANNELS,
                       rate=self.RATE,
                       input=True,
                       frames_per_buffer=self.CHUNK)
        
        print('Listening... Speak now!')
        
        frames = []
        silent_chunks = 0
        is_speaking = False
        
        while True:
            data = stream.read(self.CHUNK)
            array_data = array('h', data)
            max_volume = max(abs(vol) for vol in array_data)
            
            # If sound is above threshold, record
            if max_volume > self.SILENCE_THRESHOLD:
                is_speaking = True
                silent_chunks = 0
                frames.append(data)
            
            # If we were speaking but now there's silence
            elif is_speaking:
                frames.append(data)
                silent_chunks += 1
                
                # If enough silence, stop recording
                if silent_chunks > self.SILENCE_CHUNKS:
                    break
        
        print('Done recording')
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        return frames
