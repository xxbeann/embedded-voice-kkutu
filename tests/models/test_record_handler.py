import wave
from embedded_voice_kkutu.models.io.record_handler import RecordHandler


def save_to_wav_file(frames, filename, channels, rate):
    """녹음된 오디오 데이터를 WAV 파일로 저장"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # pyaudio.paInt16은 2바이트
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))


def main():
    """RecordHandler 테스트 및 실행"""
    # RecordHandler 객체 생성
    handler = RecordHandler()

    # 사용자에게 음성 녹음 시작 알림
    print("테스트 시작! 말을 하고, 멈추면 자동으로 중단됩니다.")

    # 음성 녹음 실행
    frames = handler.record_until_silence()

    # 결과 처리
    if len(frames) > 0:
        print(f"녹음 성공! 총 {len(frames)}개의 오디오 프레임이 캡처되었습니다.")

        # 녹음된 데이터를 WAV 파일로 저장
        output_filename = "test_output.wav"
        save_to_wav_file(frames, output_filename, handler.CHANNELS, handler.RATE)
        print(f"녹음 데이터를 '{output_filename}' 파일로 저장했습니다!")
    else:
        print("녹음 실패! 오디오 프레임이 없습니다.")


if __name__ == "__main__":
    main()
