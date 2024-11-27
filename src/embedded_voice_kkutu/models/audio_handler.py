import pyaudio
from array import array

class AudioHandler:
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    CHANNELS = 1
    RATE = 44100
    SILENCE_THRESHOLD = 1000
    SILENCE_CHUNKS = 30

    def __init__(self):
        self.format = AudioHandler.FORMAT
        self.chunk = AudioHandler.CHUNK
        self.channels = AudioHandler.CHANNELS
        self.rate = AudioHandler.RATE
        self.silence_threshold = AudioHandler.SILENCE_THRESHOLD
        self.silence_chunks = AudioHandler.SILENCE_CHUNKS
        pass
    
    def record_until_silence(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                             channels=self.channels,
                             rate=self.rate,
                             input=True,
                             frames_per_buffer=self.chunk)
        
        print('(Debug) Listening... Speak now!')

        frames = []
        silent_chunks = 0
        is_speaking = False

        while True:
            data = stream.read(self.chunk)
            array_data = array('h', data)
            max_volume = max(abs(vol) for vol in array_data)

            if max_volume > self.silence_threshold:
                is_speaking = True
                silent_chunks = 0
                frames.append(data)

            elif is_speaking:
                frames.append(data)
                silent_chunks += 1

                if silent_chunks > self.silence_chunks:
                    break
        
        print('(Debug) Done recording')

        stream.stop_stream()
        stream.close()
        p.terminate()
        return frames

    def process_audio(self, frames):
        print('(Debug) Processing audio...')

        # Placeholder for your audio processing

        return frames
    
    def play_audio(self, frames):
        print('(Debug) Playing audio...')

        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        output=True)
        
        for frame in frames:
            stream.write(frame)

        stream.stop_stream()
        stream.close()
        p.terminate()

        print('(Debug) Done playing audio')

def main():
    audio_handler = AudioHandler()
    while True:
        frames = audio_handler.record_until_silence()
        processed_frames = audio_handler.process_audio(frames)
        audio_handler.play_audio(processed_frames)

if __name__ == '__main__':
    main()
