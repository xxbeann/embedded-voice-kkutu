import speech_recognition as sr

def recognize_speech_from_mic():
    # Recognizer와 Microphone 객체 생성
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        # 마이크로부터 입력 초기화
        print("Adjusting for ambient noise... 잠시 기다려 주세요.")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("음성을 입력하세요...")
            audio = recognizer.listen(source)

        # 음성을 텍스트로 변환
        print("음성 변환 중...")
        text = recognizer.recognize_google(audio, language="ko-KR")  # 한국어 설정
        print(f"인식된 텍스트: {text}")
        return text

    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"Google Speech Recognition 서비스에 접근할 수 없습니다: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    recognize_speech_from_mic()
