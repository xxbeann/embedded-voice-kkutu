import sys
import os
from vosk import Model, KaldiRecognizer
from embedded_voice_kkutu.models.io import RecordHandler  # RecordHandler를 불러옵니다.

# Step 1: Vosk 모델 초기화 (모델 파일 경로를 지정하세요)
MODEL_PATH = "assets\vosk-model-small-ko-0.22"  # 다운로드한 모델 폴더 경로 지정
if not os.path.exists(MODEL_PATH):
    print(f"모델 경로가 올바르지 않습니다: {MODEL_PATH}")
    sys.exit(1)

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)  # 샘플 레이트 16kHz로 설정

# Step 2: Frames 데이터를 Vosk 모델에 넣기
def recognize_audio(frames, rate=16000):

    # Recognizer에 오디오 데이터를 계속 넣어서 처리
    for frame in frames:
        if recognizer.AcceptWaveform(frame):
            result = recognizer.Result()
            print("Partial Result:", result)  # 중간 결과 출력
        else:
            print("Continuing Recognition...")

    # 최종 결과 반환
    final_result = recognizer.FinalResult()
    return final_result


def main():
    # Step 3: RecordHandler를 사용하여 음성 녹음
    handler = RecordHandler()
    print("녹음을 시작합니다. 말을 멈추면 녹음이 종료됩니다.")
    frames = handler.record_until_silence()

    # Step 4: 녹음된 frames 데이터를 Vosk 모델로 전달
    if len(frames) > 0:
        print("녹음이 완료되었습니다. 음성 인식 중...")
        result = recognize_audio(frames)
        print("인식 결과:", result)
    else:
        print("녹음된 오디오 데이터가 없습니다.")


if __name__ == "__main__":
    main()