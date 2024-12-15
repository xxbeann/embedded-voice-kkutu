import os
from vosk import Model, KaldiRecognizer
from embedded_voice_kkutu.models.io import RecordHandler  # RecordHandler를 불러옵니다.


class STTHandler:
    """음성 인식(STT)을 처리하는 핸들러 클래스"""

    DEFAULT_MODEL_PATH = "assets/vosk-model-small-ko-0.22"
    DEFAULT_SAMPLE_RATE = 16000

    def __init__(self, model_path=None, sample_rate=None):
        """
        STTHandler 초기화
        - model_path: Vosk 모델 경로 (기본값: DEFAULT_MODEL_PATH)
        - sample_rate: 오디오 샘플 레이트 (기본값: DEFAULT_SAMPLE_RATE)
        """
        self.model_path = model_path or self.DEFAULT_MODEL_PATH
        self.sample_rate = sample_rate or self.DEFAULT_SAMPLE_RATE

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"모델 경로가 올바르지 않습니다: {self.model_path}")

        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

    def recognize_audio(self, frames):
        """
        오디오 데이터를 STT로 변환
        - frames: 녹음된 오디오 데이터 (PCM 바이트 데이터 리스트)
        - 반환값: STT 결과 문자열
        """
        for frame in frames:
            if self.recognizer.AcceptWaveform(frame):
                result = self.recognizer.Result()
                print("Partial Result:", result)  # 중간 결과 출력 (디버깅용)

        # 최종 결과 반환
        final_result = self.recognizer.FinalResult()
        return final_result

    def record_and_recognize(self):
        """
        음성을 녹음하고 바로 STT를 수행
        - 반환값: STT 결과 문자열
        """
        handler = RecordHandler()
        print("녹음을 시작합니다. 말을 멈추면 녹음이 종료됩니다.")
        frames = handler.record_until_silence()

        if len(frames) > 0:
            print("녹음이 완료되었습니다. 음성 인식 중...")
            return self.recognize_audio(frames)
        else:
            print("녹음된 오디오 데이터가 없습니다.")
            return None