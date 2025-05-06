from faster_whisper import WhisperModel
import tkinter as tk
from tkinter import scrolledtext
import os

from libraries import recordLIB, sentiment_analysisLIB,transcribeLIB
rc = recordLIB.rcn()

if __name__ == "__main__":
    input_mp3 = "tempR.mp3"  

    try:
        transcription = transcribeLIB.transcribe_audio_with_faster_whisper(input_mp3)

        print(transcription)
        print("sentiment...")

        sentiment_analysisLIB.analyze_emotion(transcription)
    finally:
        if os.path.exists(input_mp3):
            os.remove(input_mp3)