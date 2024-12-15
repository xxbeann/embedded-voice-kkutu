from os import path
from sys import stderr
from typing import Optional

MODEL_NAMES = [
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "medium",
    "medium.en",
    "large-v1",
    "large-v2",
    "large-v3",
    "large-v3-turbo",
    "turbo",
    "distil-large-v2",
    "distil-large-v3",
    "distil-medium.en",
    "distil-small.en",
]


def validate_model_directory(dir_path: str, download_on_fails: Optional[str] = "base"):
    if dir_path:
        model_filename = path.join(dir_path, "model.bin")
        if not path.exists(model_filename):
            stderr.write(f"Model file '{model_filename}' does not exists\n")
            return
        model_dir = dir_path
    else:
        if download_on_fails not in MODEL_NAMES:
            stderr.write(
                f"Model '{download_on_fails}' is not in the list of available models\n"
            )
            return
        model_dir = download_on_fails
    return model_dir
