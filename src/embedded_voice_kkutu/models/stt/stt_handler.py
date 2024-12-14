import whisper
import wave
from embedded_voice_kkutu.models.io import RecordHandler


# 음성 인식(STT)을 처리하는 핸들러 클래스 (Whisper 사용)
class STTHandler:

    # Whisper 모델 (tiny, base, small, medium, large 중 선택)
    DEFAULT_MODEL_NAME = "base"

    # STTHandler 초기화 - model_name: Whisper 모델 이름 (기본값: DEFAULT_MODEL_NAME)
    def __init__(self, model_name=None):

        self.model_name = model_name or self.DEFAULT_MODEL_NAME
        # Whisper 모델 로드
        print(f"Whisper 모델 '{self.model_name}' 로드 중...")
        self.model = whisper.load_model(self.model_name)
        print("모델 로드 완료.")

    # 녹음된 오디오 데이터를 WAV 파일로 저장
    # - frames: 녹음된 오디오 데이터 (PCM 바이트 데이터 리스트)
    # - sample_rate: 오디오 샘플 레이트
    # - output_path: 저장할 WAV 파일 경로
    def save_audio_to_wav(self, frames, sample_rate, output_path="recorded_audio.wav"):

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(sample_rate)
            wf.writeframes(b"".join(frames))
        return output_path

    # WAV 파일을 Whisper로 STT 처리
    # - audio_path: STT를 수행할 WAV 파일 경로
    # - 반환값: STT 결과 문자열
    def recognize_audio(self, audio_path):

        print(f"'{audio_path}' 파일에 대해 음성 인식 중...")
        result = self.model.transcribe(audio_path, language="ko")  # 한국어 설정
        return result["text"]

    # 음성 녹음 및 STT 수행
    # - 반환값: STT 결과 문자열
    def record_and_recognize(self):

        handler = RecordHandler()
        print("녹음을 시작합니다. 말을 멈추면 녹음이 종료됩니다.")
        frames = handler.record_until_silence()

        if len(frames) > 0:
            print("녹음이 완료되었습니다. WAV 파일로 저장 중...")
            audio_path = self.save_audio_to_wav(frames, sample_rate=16000)
            print("WAV 파일 저장 완료. 음성 인식 중...")
            return self.recognize_audio(audio_path)
        else:
            print("녹음된 오디오 데이터가 없습니다.")
            return None
