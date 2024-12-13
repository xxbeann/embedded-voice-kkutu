import os
from gtts import gTTS
import pygame


# 텍스트를 음성으로 변환(TTS)하고 재생하는 핸들러 클래스
class TTSHandler:

    # TTS 핸들러 초기화(생성자)
    def __init__(self, lang="ko"):
        self.lang = lang
        pygame.mixer.init()  # Pygame 오디오 초기화

    # 언어 설정 변경 메서드
    def set_language(self, lang: str):
        self.lang = lang

    # 텍스트를 음성으로 변환하고 재생하는 메서드
    def text_to_speech(self, text: str):
        if not text.strip():
            raise ValueError("텍스트가 비어있습니다. 음성을 생성할 수 없습니다.")

        # TTS로 텍스트를 음성으로 변환하여 파일 저장
        tts = gTTS(text, lang=self.lang)
        temp_file = "temp_tts.mp3"
        tts.save(temp_file)

        # MP3 파일 재생
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        # 오디오가 끝날 때까지 대기
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # 임시 파일 삭제
        os.remove(temp_file)