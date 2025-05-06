from faster_whisper import WhisperModel



def transcribe_audio_with_faster_whisper(file_path):
    """
    Transcribe the audio file using Faster Whisper and return the transcription.
    """
    model_size = "tiny"

    # Run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(file_path, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    # Combine all segments into a single transcription string
    transcription = ""
    for segment in segments:
        transcription += "[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text)

    return transcription
