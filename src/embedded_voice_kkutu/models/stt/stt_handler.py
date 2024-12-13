import os
import sys
from vosk import Model, KaldiRecognizer
from embedded_voice_kkutu.models.io import RecordHandler

class STTHandler:
    def __init__(self, model_path="assets/vosk-model-small-ko-0.22"):
        self.model_path = model_path
        self.record_handler = RecordHandler()
        self._initialize_model()

    def _initialize_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"모델 경로가 올바르지 않습니다: {self.model_path}")
        
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def recognize_audio(self, frames, rate=16000):
        partial_results = []
        
        for frame in frames:
            if self.recognizer.AcceptWaveform(frame):
                result = self.recognizer.Result()
                partial_results.append(result)
        
        final_result = self.recognizer.FinalResult()
        return final_result, partial_results

    def record_and_recognize(self):
        """음성을 녹음하고 인식하는 메소드"""
        frames = self.record_handler.record_until_silence()
        
        if not frames:
            return None, "녹음된 오디오 데이터가 없습니다."
        
        final_result, _ = self.recognize_audio(frames)
        return final_result, None