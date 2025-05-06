import os

from libraries import recordLIB, sentiment_analysisLIB,transcribeLIB
rc = recordLIB.rcn()

def main():
    input_mp3 = "tempR.mp3"  

    try:
        transcription = transcribeLIB.transcribe_audio_with_faster_whisper(input_mp3)

        return transcription,sentiment_analysisLIB.analyze_emotion(transcription)

    finally:
        if os.path.exists(input_mp3):
            os.remove(input_mp3)


main()