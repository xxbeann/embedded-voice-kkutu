import wave
import numpy as np

from .transcribe import Transcribe
from .config import WhisperModelConfig as wmc
from .utils import validate_model_directory


def load_from_file():
    model_dir = validate_model_directory(wmc.model_directory)

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
        wmc.audio,
        wmc.task,
        wmc.language,
        wmc.options,
    )
    return result


def load_from_buffer():
    model_dir = validate_model_directory(wmc.model_directory)

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

    with wave.open(wmc.audio, "rb") as wav_file:
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


if __name__ == "__main__":
    # load_from_file()
    print(load_from_buffer())
