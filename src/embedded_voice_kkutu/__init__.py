from .runner import GameRunner
import argparse
from whisper_ctranslate2 import wmc

def app():
    parser = argparse.ArgumentParser(description="Run the embedded voice kkutu game")
    parser.add_argument("--model", default="base", help="Model size to convert")
    args = parser.parse_args()

    # TODO: DO NOT CODE LIKE THIS
    if args.model:
        wmc.model_directory = f"models/whisper-{args.model}-ct2"
    
    game = GameRunner()
    game.run_game()
