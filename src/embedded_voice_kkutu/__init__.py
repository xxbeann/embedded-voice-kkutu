from .runner import GameRunner
import argparse
from whisper_ctranslate2 import wmc
from embedded_voice_kkutu.models.io import RecordLibrary


def app():
    parser = argparse.ArgumentParser(description="Run the embedded voice kkutu game")
    parser.add_argument("--model", default="base", help="Model size to convert")
    parser.add_argument(
        "--record-engine",
        default="pyaudio",
        choices=["pyaudio", "sounddevice"],
        help="Record engine to use",
    )
    parser.add_argument(
        "--disable-voice", action="store_true", help="Disable voice recognition"
    )
    parser.add_argument(
        "--disable-stdin", action="store_true", help="Disable stdin input"
    )

    args = parser.parse_args()

    # TODO: DO NOT CODE LIKE THIS
    if args.model:
        wmc.model_directory = f"models/whisper-{args.model}-ct2"

    disable_voice = False
    disable_stdin = False
    if args.disable_voice:
        disable_voice = True
    if args.disable_stdin:
        disable_stdin = True

    record_library = RecordLibrary.pyaudio
    if args.record_engine == "sounddevice":
        record_library = RecordLibrary.sounddevice
    elif args.record_engine == "pyaudio":
        record_library = RecordLibrary.pyaudio

    game = GameRunner(record_library=record_library)
    game.run_game(disable_voice, disable_stdin)
