import unittest
import json
from embedded_voice_kkutu.models.stt import STTHandler

class TestSTTHandler(unittest.TestCase):
    def setUp(self):
        self.stt_handler = STTHandler()

    def test_initialization(self):
        """STTHandler 초기화 테스트"""
        self.assertIsNotNone(self.stt_handler.model)
        self.assertIsNotNone(self.stt_handler.recognizer)

    def test_record_and_recognize(self):
        """실제 음성 녹음 및 인식 테스트"""
        print("\n음성을 녹음합니다. 아무 말이나 하세요...")
        result, error = self.stt_handler.record_and_recognize()
        
        if error:
            print(f"에러 발생: {error}")
        else:
            result_dict = json.loads(result)
            self.assertIn('text', result_dict)
            print(f"인식된 텍스트: {result_dict['text']}")

def main():
    unittest.main()

if __name__ == "__main__":
    main()