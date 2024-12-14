from embedded_voice_kkutu.models.stt import STTHandler  # 수정된 STTHandler를 불러옵니다.

# STTHandler 테스트 함수
def main():

    try:
        # STTHandler 초기화 (Whisper 모델 로드)
        print("Whisper 모델을 로드 중입니다...")
        stt_handler = STTHandler(model_name="base")  # Whisper 모델 이름 지정 ("tiny", "base", "small", etc.)
        print("Whisper 모델 로드 완료!")

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