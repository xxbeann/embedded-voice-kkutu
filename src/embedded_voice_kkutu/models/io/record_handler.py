import pyaudio
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
    """오디오 녹음을 처리하는 핸들러 클래스"""

    CHUNK = 1024  # 오디오 데이터 버퍼 크기
    FORMAT = pyaudio.paInt16  # 오디오 포맷
    CHANNELS = 1  # 모노
    RATE = 16000  # 샘플링 레이트
    SILENCE_THRESHOLD = 100  # 무음 기준 볼륨
    SILENCE_CHUNKS = 5  # 무음 지속 길이
    INITIAL_SILENCE_DURATION = 5  # 초기 무음 허용 시간 (초)
    RECORD_PREVIOUS_TEMP_TIME = 0.5  # 이전 녹음 시간

    def __init__(self):
        # print('RecordHandler initialized with pyaudio')
        return

    def calculate_rms(self, data):
        """RMS 에너지 계산: 데이터의 평균 에너지를 계산"""
        if len(data) == 0:
            return 0  # 데이터가 비어 있으면 RMS는 0
        squares = [sample * sample for sample in data]
        mean_square = sum(squares) / len(data)
        return sqrt(max(mean_square, 0))  # 음수 방지

    def validate_data(self, data):
        """데이터 유효성 검사"""
        if len(data) == 0:
            return False
        # 데이터에 이상값이 포함되어 있는지 확인
        if any(abs(sample) > 32767 for sample in data):  # paInt16 범위 초과 확인
            return False
        return True

    def record_until_silence(self):
        """
        사용자 음성을 녹음하고, 무음 기준값을 초과하는 데이터만 기록.
        초기 무음 지속 시 녹음을 종료.
        """
        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

        buffer_size = int(self.RATE * self.RECORD_PREVIOUS_TEMP_TIME / self.CHUNK)
        previous_frames = deque(maxlen=buffer_size)
        frames = []
        silent_chunks = 0
        is_speaking = False
        initial_silence_start = time.time()  # 초기 무음 감지 시작 시간

        while True:
            try:
                data = stream.read(self.CHUNK)
                array_data = array("h", data)

                # 데이터 유효성 검사
                if not self.validate_data(array_data):
                    print("Invalid data detected, skipping...")
                    continue

                # 데이터를 float으로 변환하여 오버플로우 방지
                float_data = [float(sample) for sample in array_data]
                rms = self.calculate_rms(float_data)

                # 초기 무음 상태 체크
                if is_adjust_mode:
                    print(is_speaking, rms, self.SILENCE_THRESHOLD)
                if not is_speaking:
                    previous_frames.append(data)
                    if (
                        time.time() - initial_silence_start
                        > self.INITIAL_SILENCE_DURATION
                    ):
                        break
                    if rms > self.SILENCE_THRESHOLD:
                        is_speaking = True
                        frames.extend(previous_frames)
                        frames.append(data)
                else:
                    if rms > self.SILENCE_THRESHOLD:
                        silent_chunks = 0
                        frames.append(data)
                    else:
                        silent_chunks += 1
                        if silent_chunks > self.SILENCE_CHUNKS:
                            break
                        frames.append(data)

            except Exception as e:
                print(f"Error recording: {e}")
                break

        # 스트림 종료
        stream.stop_stream()
        stream.close()

        if is_adjust_mode:
            import wave
            from datetime import datetime
            from pathlib import Path

            Path(".out").mkdir(parents=True, exist_ok=True)
            wf = wave.open(f".out/{datetime.now()}.tmp.wav", "wb")
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(frames))
            wf.close()

        p.terminate()
        return frames


if __name__ == "__main__":
    record_handler = RecordHandler()
    frames = record_handler.record_until_silence()
    print(frames)
