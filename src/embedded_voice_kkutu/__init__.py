import json
from typing import Dict, List


def load_word_dictionary() -> Dict[str, List[str]]:
    try:
        with open("assets/words.json", "r", encoding="utf-8") as f:
            data = json.load(f)

            return data
    except Exception as e:
        print(f"단어 사전 로드 실패: {e}")
        return {}


def hello() -> str:
    word_dict = load_word_dictionary()

    if "words_list" in word_dict:
        words = word_dict["words_list"]
        print(f"단어 데이터 로드 완료: {len(words)}개의 단어를 불러왔습니다.")
        print("단어 예시:", words[:5])
    else:
        print("단어 목록을 찾을 수 없습니다.")

    return "Hello from embedded-voice-kkutu!!"
