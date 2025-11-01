import asyncio
import sounddevice as sd
import numpy as np
import soundfile as sf
import asyncio
from groq import Groq
import time
import os
from collections import deque
import webrtcvad 
from dotenv import load_dotenv

# Initialize VAD with aggressiveness mode (3 is most aggressive)
vad = webrtcvad.Vad(3)
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


async def capture_audio(filename="stt_transcribe.flac"):
    fs = 16000  # Must be 16000 for webrtcvad
    chunk_duration = 30  # ms
    chunk_size = int(fs * chunk_duration / 1000)
    silence_timeout = 1.0  # Seconds of silence to stop
    buffer = []
    audio_queue = deque()
    silent_chunks = 0
    
    print("Listening... (Speak now)")
    
    def callback(indata, frames, time, status):
        # Convert float32 to int16 for VAD
        int16_data = (indata * 32767).astype(np.int16)
        audio_queue.append(int16_data.copy())
    
    with sd.InputStream(samplerate=fs, channels=1, dtype=np.float32,blocksize=chunk_size, callback=callback):
        time.sleep(0.5)
        while True:
            if len(audio_queue) > 0:
                chunk = audio_queue.popleft()
                # Check voice activity
                if vad.is_speech(chunk.tobytes(), fs):
                    buffer.append(chunk)
                    silent_chunks = 0
                else:
                    silent_chunks += 1
                
                # Stop after 1 second of silence
                if silent_chunks > (1 / (chunk_duration / 1000)):
                    break
    
    if len(buffer) == 0:
        print("No speech detected\n")
        return None
    
    # Save recording
    full_audio = np.concatenate(buffer)
    output_dir = "Testing/audio_files"
    os.makedirs(output_dir, exist_ok=True)
    full_filename = os.path.join(output_dir, filename)
    
    # Convert back to float32 for saving
    float_audio = full_audio.astype(np.float32) / 32767.0
    sf.write(full_filename, float_audio, fs, format='FLAC')
    
    return full_filename
         
async def transcribe_audio(filename, language):
    with open(filename, "rb") as file:
        response = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            language=language,
            temperature=0,
            response_format="verbose_json",
        )
    return response.text
        

# Dictionary with languages and their shortcut codes, including English as default
LANGUAGE_SHORTCUTS = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Assamese": "as",
    "Urdu": "ur"
}

# Updated function using indexing, with fallback for missing keys
async def capture_and_transcribe_audio(input_lang):
    # Use indexing for explicit key access
    try:
        lang_code = LANGUAGE_SHORTCUTS[input_lang]
    except KeyError:
        raise ValueError(f"Unexpected language: {input_lang}")
    audio_file = await capture_audio()
    if not audio_file:
        return None
    transcribed_text = await transcribe_audio(audio_file, language=lang_code)
    if 'watching' in transcribed_text or "Let's go" in transcribed_text:
        return None
    return transcribed_text




