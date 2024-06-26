import os
import subprocess
from deepspeech import Model
import wave
import numpy as np

def download_youtube_video(url, output_path='video.mp4'):
    from pytube import YouTube
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=output_path)
    return output_path

def convert_video_to_wav_ffmpeg(video_path, audio_path):
    command = ['ffmpeg', '-i', video_path, '-ar', '16000', '-ac', '1', audio_path]
    subprocess.run(command, check=True)

def transcribe_audio_deepspeech(model_path, scorer_path, audio_path):
    model = Model(model_path)
    model.enableExternalScorer(scorer_path)

    with wave.open(audio_path, 'rb') as wf:
        assert wf.getnchannels() == 1  # DeepSpeech expects mono audio
        assert wf.getsampwidth() == 2  # DeepSpeech expects 16-bit audio
        assert wf.getframerate() == 16000  # DeepSpeech expects 16kHz audio

        audio = np.frombuffer(wf.readframes(wf.getnframes()), np.int16)
        text = model.stt(audio)
        with open("archivo.txt", "w") as archivo:
                archivo.write(text)
        return text

def transcribe_youtube_video(url, model_path, scorer_path):
    video_path = "video.mp4" #download_youtube_video(url)
    audio_path = 'audio.wav'
    # convert_video_to_wav_ffmpeg(video_path, audio_path)
    text = transcribe_audio_deepspeech(model_path, scorer_path, audio_path)

    # # Cleanup the downloaded files
    # os.remove(video_path)
    # os.remove(audio_path)
    
    return text

# Example usage
youtube_url = "https://www.youtube.com/watch?v=HbnTFIMePVs&t=4s"
model_path = r'deep/deepspeech-0.9.3-models.pbmm'  # Path to the model file
scorer_path = r'deep/deepspeech-0.9.3-models.scorer'  # Path to the scorer file
transcription = transcribe_youtube_video(youtube_url, model_path, scorer_path)
print(transcription)
