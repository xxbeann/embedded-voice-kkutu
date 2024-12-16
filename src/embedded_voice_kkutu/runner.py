import json
from typing import Dict, List, Set
from .service.game_service import WordChainGame
from .models.io import ConcurrencyIO, RecordLibrary
from threading import Event

DEBUG = True


def on_audio_record(frames: List[int]) -> Dict[str, List[int]]:
    return {"frames": frames}


class GameRunner:
    def __init__(
        self,
        record_library: RecordLibrary = RecordLibrary.pyaudio,
    ):
        self.game = WordChainGame()
        self.io_handler = ConcurrencyIO(
            GameRunner.on_audio_record, GameRunner.on_stdin_input, record_library
        )
        self.io_input_event = self.io_handler.event

    def on_audio_record(data):
        print(data)
        if DEBUG:
            print("__DEBUG__/on_audio_record", data)
        return "__오디오 입력__"

    def on_stdin_input(input_str: str) -> str:
        if DEBUG:
            print("__DEBUG__/on_stdin_input", input_str)
        return input_str

    def _fetch_input(self) -> str:
        player_word = None
        while player_word is None:
            self.io_input_event.wait()
            try:
                player_word = self.io_handler.fetch().data.strip()
            except IndexError:
                continue
        return player_word

    def run_game(
        self, disable_voice: bool = False, disable_stdin: bool = False
    ) -> None:
        next_word = None

        print("끝말잇기를 시작합니다! 게임을 종료하려면 '종료'를 입력하세요.")
        self.io_handler.start_io(disable_voice, disable_stdin)  # Start the IO threads
        self.io_input_event.clear()  # Reset the event
        print("첫 단어를 입력하세요: ", end="", flush=True)
        player_word = self._fetch_input()
        if DEBUG:
            print("__DEBUG__/run_game/on_first_input", player_word)

        while True:
            if player_word == "종료":
                print("게임을 종료합니다!")
                self.io_handler.close_event.set()
                self.io_handler.join_io()
                exit(0)

            # 플레이어 입력 단어가 유효한지 확인
            if not self.game.is_valid_word(next_word, player_word):
                print("유효한 단어가 아닙니다. 다시 입력해주세요.", end="", flush=True)
                player_word = self._fetch_input()
                if DEBUG:
                    print("__DEBUG__/run_game/on_retry", player_word)
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
                print("__DEBUG__/run_game/game_continued", player_word)
