from typing import Callable, TypeVar, Union
from enum import Enum
import threading
from collections import deque

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

    def start_audio_record(self):
        while not self.close_event.is_set():
            frames: list = self.record_handler.record_until_silence()
            data = frames

            if self.audio_record_callback:
                data = self.audio_record_callback(frames)

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

    def start_io(self):
        self.audio_record_thread = threading.Thread(target=self.start_audio_record)
        self.stdin_input_thread = threading.Thread(target=self.start_stdin_input)

        self.audio_record_thread.start()
        self.stdin_input_thread.start()

    def join_io(self):
        self.join_audio_record()
        self.join_stdin_input()

    def fetch(self):
        if self.record_result:
            return self.record_result.popleft()
        raise IndexError("No record to fetch")
