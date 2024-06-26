import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import speech_recognition as sr

def download_youtube_video(url, output_path='video.mp4'):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=output_path)
    return output_path

def extract_audio(video_path, audio_path='audio.wav'):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def transcribe_youtube_video(url):
    video_path = "video.mp4" #download_youtube_video(url)
    audio_path = extract_audio(video_path)
    text = transcribe_audio(audio_path)
    
    # Cleanup the downloaded files
    os.remove(video_path)
    os.remove(audio_path)
    
    return text

# Example usage
youtube_url = "https://www.youtube.com/watch?v=HbnTFIMePVs&t=4s"
transcription = transcribe_youtube_video(youtube_url)
print(transcription)
