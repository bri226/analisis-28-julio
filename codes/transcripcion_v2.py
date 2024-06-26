import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import subprocess
import traceback

def download_youtube_video(url, output_path='video.mp4'):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=output_path)
    return output_path

def convert_video_to_wav_ffmpeg(video_path, audio_path):
    command = ['ffmpeg', '-i', video_path, audio_path]
    subprocess.run(command, check=True)
    print("Convert video to wav")

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source,duration=4)
        try:
            text = recognizer.recognize_google(audio, language = 'es-US', show_all=True)
            with open("archivo.txt", "w") as archivo:
                archivo.write(text)
            return text
        
        except sr.UnknownValueError as e:
            traceback.print_exc()
            return f"Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def transcribe_youtube_video(url):
    # video_path = download_youtube_video(url)
    video_path = "video.mp4"
    audio_path = 'audio.wav'
    # convert_video_to_wav_ffmpeg(video_path, audio_path)
    text = transcribe_audio(audio_path)
    
    # # Cleanup the downloaded files
    # os.remove(video_path)
    # os.remove(audio_path)
    
    return text

# Example usage
youtube_url = "https://www.youtube.com/watch?v=HbnTFIMePVs&t=4s"
transcription = transcribe_youtube_video(youtube_url)
print(transcription)
