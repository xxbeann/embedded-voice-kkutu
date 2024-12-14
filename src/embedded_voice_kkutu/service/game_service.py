import json
from typing import Dict, List, Set, Optional
from embedded_voice_kkutu.models.ko_kr import KoKrSupport
from random import sample


def load_word_dictionary() -> Dict[str, List[str]]:
    try:
        with open("assets/words.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("words_dict", {})
    except Exception as e:
        print(f"단어 딕셔너리 로드 실패: {e}")
        return {}


class WordChainGame:
    def __init__(self):
        self.words_dict = load_word_dictionary()
        self.used_words: set[str] = set()  # 이미 사용된 단어 저장

    def is_valid_word(self, current_word: Optional[str], word: str) -> bool:
        # 첫 단어가 아닐 경우 이전 단어 마지막 글자와 입력 첫 글자가 같은 지 확인
        if current_word is not None:
            ables = [current_word[-1]]
            init_law_applied = KoKrSupport.init_law_char(current_word[-1])
            if init_law_applied != current_word[-1]:
                ables.append(init_law_applied)

            if word[0] not in ables:
                print(
                    "이전 단어의 마지막 글자 {}로 시작해야 합니다.".format(
                        ables[0]
                        if len(ables) == 1
                        else f"{ables[0]} 또는 {', '.join(ables[1:])}"
                    )
                )
                return False

        # 사전에 있는 단어인지 확인
        if word[0] not in self.words_dict or word not in self.words_dict[word[0]]:
            print("사전에 없는 단어입니다.")
            return False

        # 이미 사용한 단어인지 확인
        if word in self.used_words:
            print("이미 사용한 단어입니다.")
            return False

        return True

    def get_next_word(self, last_letter: str) -> str:
        possible_words = set()
        if last_letter in self.words_dict:
            possible_words = possible_words.union(set(self.words_dict[last_letter]))
        init_law_applied = KoKrSupport.init_law_char(last_letter)
        if init_law_applied != last_letter and init_law_applied in self.words_dict:
            possible_words = possible_words.union(
                set(self.words_dict[init_law_applied])
            )

        remains = len(possible_words)
        rejected = set()

        while remains > len(rejected):
            word = sample(possible_words, 1)
            if len(word) == 0:
                break
            word = word[0]

            if word not in self.used_words:
                self.used_words.add(word)
                return word
            else:
                rejected.add(word)

        return None

    def play_turn(self, player_word: str) -> str:
        last_letter = player_word[-1]
        next_word = self.get_next_word(last_letter)
        if next_word:
            print(f"컴퓨터의 단어: {next_word}")
            return next_word
        else:
            print("컴퓨터가 더 이상 단어를 찾을 수 없습니다!")
            return None
