import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper
import time
import datetime
import subprocess

def download_youtube_video(url, output_path='video.mp4'):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=output_path)
    print("Video downloaded.")
    return output_path

def convert_video_to_wav_ffmpeg(video_path, audio_path):
    command = ['ffmpeg', '-i', video_path, audio_path]
    subprocess.run(command, check=True)
    print("Convert video to wav")

# def convert_video_to_wav(video_path, audio_path='audio.wav'):
#     video = VideoFileClip(video_path)
#     video.audio.write_audiofile(audio_path)
#     print("Audio converted.")
#     return audio_path

def transcribe_audio_with_whisper(audio_path, language='es'):
    print(f"Empezó transcripción, {datetime.datetime.now()}")
    # model = whisper.load_model("base")  # You can use "base", "small", "medium", "large"
    model_path = "base.pt"  #"small.pt"
    model = whisper.load_model(model_path)
    result = model.transcribe(audio_path, language=language)
    print("Entró a transcribe_audio_with_whisper")
    with open("archivo.txt", "w", encoding="utf-8") as archivo:
        archivo.write(result["text"])
    print(f"Terminó transcripción, {datetime.datetime.now()} ")
    return result["text"]


def transcribe_youtube_video(url):
    inicio = time.time()
    video_path = "video.mp4" #download_youtube_video(url)
    audio_path = 'audio.wav'
    # convert_video_to_wav_ffmpeg(video_path,audio_path)
    text = transcribe_audio_with_whisper(audio_path, language='es')
    fin = time.time()
    # os.remove(video_path)
    # os.remove(audio_path)
    print(f"Tiempo total: {round(fin-inicio,2)} ")
    return text

# # Example usage
# youtube_url = "https://www.youtube.com/watch?v=HbnTFIMePVs&t=4s" #VIZCARRA
youtube_url = "https://www.youtube.com/watch?v=ja1lpgtwcOQ" #DINA

transcription = transcribe_youtube_video(youtube_url)
# print(transcription)
print("Terminoooo")
# 10:08
