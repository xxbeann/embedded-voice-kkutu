from embedded_voice_kkutu.models.tts import TTSHandler

# 테스트 코드
def main():
    # TTSHandler 객체 생성 (기본 언어: 한국어)
    tts_handler = TTSHandler()

    # # 텍스트를 음성으로 출력
    tts_handler.text_to_speech("안녕하세요. TTS 핸들러입니다.")

    # 언어를 영어로 변경 후 테스트
    # tts_handler.set_language("en")
    # tts_handler.text_to_speech("Hello, this is a TTS handler.")


if __name__ == "__main__":
    main()