import pyaudio
import wave
import threading
import sys
import queue

class AudioHandler:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.input_queue = queue.Queue()

    def start_recording(self):
        self.is_recording = True
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        print("녹음 시작...")
        
        while self.is_recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        # 녹음 저장
        wf = wave.open('output.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print("녹음 완료")

    def input_handler(self):
        while True:
            try:
                user_input = input()
                self.input_queue.put(user_input)
                if user_input.lower() == 'q':
                    break
            except EOFError:
                break

def main():
    audio_handler = AudioHandler()
    
    # 오디오 녹음 스레드
    record_thread = threading.Thread(target=audio_handler.start_recording)
    # 입력 처리 스레드
    input_thread = threading.Thread(target=audio_handler.input_handler)
    
    record_thread.start()
    input_thread.start()
    
    try:
        while True:
            if not audio_handler.input_queue.empty():
                command = audio_handler.input_queue.get()
                if command.lower() == 'q':
                    audio_handler.stop_recording()
                    break
                print(f"입력받은 명령어: {command}")
    
    except KeyboardInterrupt:
        audio_handler.stop_recording()
    
    record_thread.join()
    input_thread.join()
    audio_handler.audio.terminate()

if __name__ == "__main__":
    main()
