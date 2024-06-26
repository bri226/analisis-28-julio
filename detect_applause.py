import librosa
import numpy as np

def detect_applause(audio_path, threshold=0.2, frame_length=2048, hop_length=512):
    # Load the audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Compute the short-time energy of the audio signal
    energy = np.array([
        sum(abs(y[i:i+frame_length]**2))
        for i in range(0, len(y), hop_length)
    ])
    
    # Normalize the energy values
    energy = energy / np.max(energy)
    
    # Identify frames where the energy exceeds the threshold
    applause_frames = np.where(energy > threshold)[0]
    
    # Convert frame indices to time in seconds
    applause_times = applause_frames * hop_length / sr
    
    # Group applause times to identify distinct applause events
    applause_events = []
    current_event = []
    for t in applause_times:
        if not current_event or t - current_event[-1] < 1:
            current_event.append(t)
        else:
            applause_events.append(current_event)
            current_event = [t]
    if current_event:
        applause_events.append(current_event)
    
    # Extract the start time of each applause event
    applause_start_times = [event[0] for event in applause_events]
    
    return applause_start_times

# Usage
audio_path = 'path_to_your_audio.wav'
applause_times = detect_applause(audio_path)
print(f"Aplausos detectados en los siguientes segundos: {applause_times}")
