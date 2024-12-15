import json
from typing import Dict, List, Set
from .service.game_service import WordChainGame
from .models.io import ConcurrencyIO
from threading import Event

DEBUG = True


def on_audio_record(frames: List[int]) -> Dict[str, List[int]]:
    return {"frames": frames}


def on_stdin_input(input_str: str) -> str:
    print(input_str)
    return input_str


class GameRunner:
    def __init__(self):
        self.game = WordChainGame()
        self.io_handler = ConcurrencyIO(self.on_audio_record, on_stdin_input)
        self.io_input_event = self.io_handler.event

    def on_audio_record(obj, frames: List[int]):
        return "__오디오 입력__"

    def _fetch_input(self) -> str:
        player_word = None
        while player_word is None:
            self.io_input_event.wait()
            try:
                player_word = self.io_handler.fetch().data.strip()
            except IndexError:
                continue
        return player_word

    def run_game(self) -> None:
        next_word = None

        print("끝말잇기를 시작합니다! 게임을 종료하려면 '종료'를 입력하세요.")
        self.io_handler.start_io()  # Start the IO threads
        self.io_input_event.clear()  # Reset the event
        print("첫 단어를 입력하세요: ", end="", flush=True)
        player_word = self._fetch_input()
        if DEBUG:
            print("__DEBUG__", player_word)

        while True:
            if player_word == "종료":
                print("게임을 종료합니다!")
                break

            # 플레이어 입력 단어가 유효한지 확인
            if not self.game.is_valid_word(next_word, player_word):
                print("유효한 단어가 아닙니다. 다시 입력해주세요.", end="", flush=True)
                player_word = self._fetch_input()
                if DEBUG:
                    print("__DEBUG__", player_word)
                continue

            # 플레이어 단어 등록
            self.game.used_words.add(player_word)

            # 컴퓨터 응답
            next_word = self.game.play_turn(player_word)
            if next_word is None:
                print("축하합니다! 당신이 이겼어용!!", flush=True)
                break

            print("단어를 입력하세요: ", flush=True)
            player_word = self._fetch_input()
            if DEBUG:
                print("__DEBUG__", player_word)
