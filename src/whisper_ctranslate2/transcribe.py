import sys
from typing import BinaryIO, List, NamedTuple, Optional, Union
import numpy as np

from faster_whisper import BatchedInferencePipeline, WhisperModel

system_encoding = sys.getdefaultencoding()

if system_encoding != "utf-8":

    def make_safe(string):
        return string.encode(system_encoding, errors="replace").decode(system_encoding)

else:

    def make_safe(string):
        return string


class TranscriptionOptions(NamedTuple):
    beam_size: int
    best_of: int
    patience: float
    length_penalty: float
    repetition_penalty: float
    no_repeat_ngram_size: int
    log_prob_threshold: Optional[float]
    no_speech_threshold: Optional[float]
    compression_ratio_threshold: Optional[float]
    condition_on_previous_text: bool
    prompt_reset_on_temperature: float
    temperature: List[float]
    initial_prompt: Optional[str]
    prefix: Optional[str]
    hotwords: Optional[str]
    suppress_blank: bool
    suppress_tokens: Optional[List[int]]
    word_timestamps: bool
    prepend_punctuations: str
    append_punctuations: str
    hallucination_silence_threshold: Optional[float]
    vad_filter: bool
    vad_onset: Optional[float]
    vad_min_speech_duration_ms: Optional[int]
    vad_max_speech_duration_s: Optional[int]
    vad_min_silence_duration_ms: Optional[int]


class Transcribe:
    @staticmethod
    def _get_vad_parameters_dictionary(options):
        vad_parameters = {}

        if options.vad_onset:
            vad_parameters["onset"] = options.vad_onset

        if options.vad_min_speech_duration_ms:
            vad_parameters["min_speech_duration_ms"] = (
                options.vad_min_speech_duration_ms
            )

        if options.vad_max_speech_duration_s:
            vad_parameters["max_speech_duration_s"] = options.vad_max_speech_duration_s

        if options.vad_min_silence_duration_ms:
            vad_parameters["min_silence_duration_ms"] = (
                options.vad_min_silence_duration_ms
            )

        return vad_parameters

    def __init__(
        self,
        model_path: str,
        device: str,
        device_index: Union[int, List[int]],
        compute_type: str,
        threads: int,
        cache_directory: str,
        local_files_only: bool,
        batched: bool,
        batch_size: int = None,
    ):
        self.model = WhisperModel(
            model_path,
            device=device,
            device_index=device_index,
            compute_type=compute_type,
            cpu_threads=threads,
            download_root=cache_directory,
            local_files_only=local_files_only,
        )

        self.batch_size = batch_size
        if batched:
            self.batched_model = BatchedInferencePipeline(model=self.model)
        else:
            self.batched_model = None

    def inference(
        self,
        audio: Union[str, BinaryIO, np.ndarray],
        task: str,
        language: str,
        options: TranscriptionOptions,
    ):
        vad_parameters = Transcribe._get_vad_parameters_dictionary(options)

        if self.batched_model:
            model = self.batched_model
            vad = True
        else:
            model = self.model
            vad = options.vad_filter

        batch_size = (
            {"batch_size": self.batch_size} if self.batch_size is not None else {}
        )

        segments, info = model.transcribe(
            audio=audio,
            language=language,
            task=task,
            beam_size=options.beam_size,
            best_of=options.best_of,
            patience=options.patience,
            length_penalty=options.length_penalty,
            repetition_penalty=options.repetition_penalty,
            no_repeat_ngram_size=options.no_repeat_ngram_size,
            temperature=options.temperature,
            compression_ratio_threshold=options.compression_ratio_threshold,
            log_prob_threshold=options.log_prob_threshold,
            no_speech_threshold=options.no_speech_threshold,
            condition_on_previous_text=options.condition_on_previous_text,
            prompt_reset_on_temperature=options.prompt_reset_on_temperature,
            initial_prompt=options.initial_prompt,
            prefix=options.prefix,
            hotwords=options.hotwords,
            suppress_blank=options.suppress_blank,
            suppress_tokens=options.suppress_tokens,
            word_timestamps=options.word_timestamps,
            prepend_punctuations=options.prepend_punctuations,
            append_punctuations=options.append_punctuations,
            hallucination_silence_threshold=options.hallucination_silence_threshold,
            vad_filter=vad,
            vad_parameters=vad_parameters,
            **batch_size,
        )

        list_segments = []
        last_pos = 0
        accumated_inc = 0
        all_text = ""

        for segment in segments:
            all_text += segment.text
            segment_dict = segment._asdict()
            if segment.words:
                segment_dict["words"] = [word._asdict() for word in segment.words]

            list_segments.append(segment_dict)
            duration = segment.end - last_pos
            increment = (
                duration
                if accumated_inc + duration < info.duration
                else info.duration - accumated_inc
            )
            accumated_inc += increment
            last_pos = segment.end

        return dict(
            text=all_text,
            segments=list_segments,
            language=info.language,
        )
