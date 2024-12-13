from embedded_voice_kkutu.models.stt import STTHandler

# 모델 초기화 (테스트 실행 시 한 번만 로드)
MODEL_PATH = "assets/vosk-model-small-ko-0.22"
SAMPLE_RATE = 16000


def main():
    """
    STTHandler 테스트 함수.
    - 음성을 녹음하고, STT 결과를 출력합니다.
    """
    try:
        # STTHandler 초기화 (모델을 한 번만 로드)
        print("모델을 로드 중입니다...")
        stt_handler = STTHandler(model_path=MODEL_PATH, sample_rate=SAMPLE_RATE)
        print("모델 로드 완료!")

        # 음성을 녹음하고 변환 결과 출력
        result = stt_handler.record_and_recognize()
        if result:
            print("STT 결과:", result)
        else:
            print("STT를 수행할 데이터가 없습니다.")

    except FileNotFoundError as e:
        print("에러:", e)
    except Exception as e:
        print("예기치 못한 에러가 발생했습니다:", e)


if __name__ == "__main__":
    main()
