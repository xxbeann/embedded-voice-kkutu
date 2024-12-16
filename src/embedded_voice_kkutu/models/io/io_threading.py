from typing import Callable, TypeVar, Union
from enum import Enum
import threading
from collections import deque
import numpy as np

import whisper_ctranslate2 as wc2
from .record_handler import RecordHandler

T = TypeVar("T")
RecordData = Union[list, str]


class RecordType(Enum):
    stdin_string = "stdin_string"
    audio_record = "audio_record"


class RecordStruct:
    def __init__(self, record_type: RecordType, data: "RecordData"):
        self.record_type = record_type
        self.data = data

    def __str__(self):
        return f"RecordStruct({self.record_type}, {self.data})"

    def __repr__(self):
        return self.__str__()


class ConcurrencyIO:
    def __init__(
        self,
        audio_record_callback: Callable[list, T],
        stdin_input_callback: Callable[str, str],
    ):
        # Type T in `audio_record_callback` will be decided when type of model's input.
        self.audio_record_callback = audio_record_callback
        self.stdin_input_callback = stdin_input_callback
        self.record_handler = RecordHandler()
        self.record_result: deque[RecordStruct] = deque()
        self.audio_record_thread: threading.Thread = None
        self.stdin_input_thread: threading.Thread = None
        self.event = threading.Event()
        self.close_event = threading.Event()

        model_dir = wc2.validate_model_directory(wc2.wmc.model_directory)
        self.transcribe = wc2.Transcribe(
            model_dir,
            wc2.wmc.device,
            wc2.wmc.device_index,
            wc2.wmc.compute_type,
            wc2.wmc.threads,
            wc2.wmc.cache_directory,
            wc2.wmc.local_files_only,
            wc2.wmc.batched,
            wc2.wmc.batch_size,
        )

    def start_audio_record(self):
        while not self.close_event.is_set():
            frames: list = self.record_handler.record_until_silence()

            audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
            audio_data = audio_data.astype(np.float32)
            if len(audio_data) > 0:
                audio_data = audio_data / 32768.0

            data = self.transcribe.inference(
                audio_data,
                wc2.wmc.task,
                wc2.wmc.language,
                wc2.wmc.options,
            )

            if self.audio_record_callback and False:
                data = self.audio_record_callback(frames)

            if "text" not in data:
                continue
            if data["text"] == "":
                continue
            data = data["text"].replace(" ", "")

            self.record_result.append(RecordStruct(RecordType.audio_record, data))
            self.event.set()

    def start_stdin_input(self):
        while not self.close_event.is_set():
            try:
                gets = input()
                data = gets

                if self.stdin_input_callback:
                    data = self.stdin_input_callback(gets)

                self.record_result.append(RecordStruct(RecordType.stdin_string, data))
                self.event.set()
            except EOFError:
                break

    def join_audio_record(self):
        if self.audio_record_thread:
            self.audio_record_thread.join()

    def join_stdin_input(self):
        if self.stdin_input_thread:
            self.stdin_input_thread.join()

    def start_io(self, disable_voice: bool = False, disable_stdin: bool = False):
        if not disable_voice:
            self.audio_record_thread = threading.Thread(target=self.start_audio_record)
            self.audio_record_thread.start()
        if not disable_stdin:
            self.stdin_input_thread = threading.Thread(target=self.start_stdin_input)
            self.stdin_input_thread.start()

    def join_io(self):
        self.join_audio_record()
        self.join_stdin_input()

    def fetch(self):
        if self.record_result:
            return self.record_result.popleft()
        raise IndexError("No record to fetch")
