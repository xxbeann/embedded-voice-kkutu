import wave
import numpy as np

from .transcribe import Transcribe
from .config import WhisperModelConfig as wmc
from .utils import validate_model_directory


def load_from_file(model=wmc.model_directory, filename=wmc.audio):
    model_dir = validate_model_directory(model)

    transcribe = Transcribe(
        model_dir,
        wmc.device,
        wmc.device_index,
        wmc.compute_type,
        wmc.threads,
        wmc.cache_directory,
        wmc.local_files_only,
        wmc.batched,
        wmc.batch_size,
    )

    result = transcribe.inference(
        filename,
        wmc.task,
        wmc.language,
        wmc.options,
    )
    return result


def load_from_buffer(model=wmc.model_directory, filename=wmc.audio):
    model_dir = validate_model_directory(model)

    transcribe = Transcribe(
        model_dir,
        wmc.device,
        wmc.device_index,
        wmc.compute_type,
        wmc.threads,
        wmc.cache_directory,
        wmc.local_files_only,
        wmc.batched,
        wmc.batch_size,
    )

    with wave.open(filename, "rb") as wav_file:
        audio_bytes = wav_file.readframes(wav_file.getnframes())

        audio_data = np.frombuffer(audio_bytes, dtype=np.int16)

        audio_data = audio_data.astype(np.float32)
        if len(audio_data) > 0:
            audio_data = audio_data / 32768.0

    result = transcribe.inference(
        wmc.audio,
        wmc.task,
        wmc.language,
        wmc.options,
    )
    return result

import argparse
def main():
    parser = argparse.ArgumentParser(description="Run the embedded voice kkutu game")
    parser.add_argument("--model", default="base", help="Model size to convert")
    parser.add_argument("--load-from-file", action="store_true", help="Load from file")
    parser.add_argument("--filename", default="audio.wav", help="Filename to load")
    args = parser.parse_args()

    model_path = f"models/whisper-{args.model}-ct2"

    if args.load_from_file:
        print(load_from_file(model_path, args.filename))
    else:
        print(load_from_buffer(model_path, args.filename))

if __name__ == "__main__":
    # load_from_file()
    # print(load_from_buffer())
    main()
