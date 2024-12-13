import json
from typing import Dict, List, Set
from .service.playGame import WordChainGame


def hello() -> str:
    game = WordChainGame()
    next_word = None

    print("끝말잇기를 시작합니다! 게임을 종료하려면 '종료'를 입력하세요.")
    player_word = input("첫 단어를 입력하세요: ").strip()

    while True:
        if player_word == "종료":
            print("게임을 종료합니다!")
            break

        # 플레이어 입력 단어가 유효한지 확인
        if not game.is_valid_word(next_word, player_word):
            player_word = input("단어를 다시 입력하세요: ").strip()
            continue

        # 플레이어 단어 등록
        game.used_words.add(player_word)

        # 컴퓨터 응답
        next_word = game.play_turn(player_word)
        if next_word is None:
            print("축하합니다! 당신이 이겼어용!!")
            break

        player_word = input(f"단어를 입력하세요: ").strip()

    return "Hello from embedded-voice-kkutu!!"
