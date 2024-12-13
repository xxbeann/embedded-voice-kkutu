import wave
from embedded_voice_kkutu.models.io import RecordHandler

if __name__ == "__main__":
    # RecordHandler 객체 생성
    handler = RecordHandler()

    # 사용자에게 음성 녹음 시작 알림
    print("테스트 시작! 말을 하고, 멈추면 자동으로 중단됩니다.")
    
    # 음성 녹음 실행
    frames = handler.record_until_silence()
    
    # 결과 출력
    if len(frames) > 0:
        print(f"녹음 성공! 총 {len(frames)}개의 오디오 프레임이 캡처되었습니다.")

        # 녹음된 데이터를 WAV 파일로 저장
        with wave.open("test_output.wav", "wb") as wf:
            wf.setnchannels(handler.CHANNELS)
            wf.setsampwidth(2)  # pyaudio.paInt16은 2바이트
            wf.setframerate(handler.RATE)
            wf.writeframes(b''.join(frames))
        print("녹음 데이터를 'test_output.wav' 파일로 저장했습니다!")
    else:
        print("녹음 실패! 오디오 프레임이 없습니다.")
    
    # 녹음된 데이터 확인
    print("녹음 데이터 샘플:", frames[:2])  # 첫 두 프레임만 출력