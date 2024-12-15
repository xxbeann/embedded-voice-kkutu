from .transcribe import TranscriptionOptions

class WhisperModelConfig:
    model: str = "small"
    threads: int = 0
    language: str = "ko"
    task: str = "transcribe"
    device: str = "cpu"
    compute_type: str = "int8"
    model_directory: str = "models/whisper-base-ct2"
    cache_directory: str = None
    device_index: int = 0
    audio: str = "realtime_audio.wav"
    local_files_only: bool = False
    batched = True
    batch_size = 2

    options = TranscriptionOptions(
        beam_size=5,
        best_of=5,
        patience=1.0,
        length_penalty=1.0,
        repetition_penalty=1.0,
        no_repeat_ngram_size=0,
        log_prob_threshold=0,
        no_speech_threshold=.6,
        compression_ratio_threshold=2.4,
        condition_on_previous_text=True,
        temperature = [0],
        prompt_reset_on_temperature=.5,
        initial_prompt=None,
        prefix=None,
        hotwords=None,
        suppress_blank=True,
        suppress_tokens = [-1],
        word_timestamps=False,
        prepend_punctuations="\"'“¿([{-",
        append_punctuations="\"'.。,，!！?？:：”)]}、",
        hallucination_silence_threshold=None,
        vad_filter=False,
        vad_onset=None,
        vad_min_speech_duration_ms=None,
        vad_max_speech_duration_s=None,
        vad_min_silence_duration_ms=None,
    )
