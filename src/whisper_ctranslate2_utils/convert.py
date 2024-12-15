from os import path
import argparse
from ctranslate2.converters import TransformersConverter

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


def convert_model(model_size="base"):
    output_dir = f"models/whisper-{model_size}-ct2"
    if path.exists(output_dir):
        print(f"Model already exists at {output_dir}")
        return
    if model_size not in MODEL_NAMES:
        raise ValueError(f"Invalid model size: {model_size}")
    converter = TransformersConverter(f"openai/whisper-{model_size}")
    converter.convert(output_dir=output_dir, quantization="int8")


def main():
    parser = argparse.ArgumentParser(
        description="Convert OpenAI's Whisper models to CTranslate2 format"
    )
    parser.add_argument(
        "--model-size",
        default="base",
        choices=MODEL_NAMES,
        help="Model size to convert",
    )
    args = parser.parse_args()
    convert_model(args.model_size)
