from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import wave
from datetime import datetime

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_2")
client = genai.Client(api_key=api_key)

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM data to WAV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    print(f"✅ Audio saved to: {filename}")
    return filename


async def gemini_tts_synthesize(text, output_file=None):
    """
    Generate speech from text using Gemini TTS.
    Gemini automatically detects and speaks the language.
    
    Args:
        text (str): Text to synthesize
        output_file (str): Optional custom output path
    
    Returns:
        str: Path to generated WAV file
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"Testing/audio_files/tts_{timestamp}.wav"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"]
            )
        )

        if response is None:
            raise Exception("API returned None")
        
        if not response.candidates or len(response.candidates) == 0:
            raise Exception("No candidates in response")
        
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        
        if not audio_data:
            raise Exception("Audio data is empty")
        
        return wave_file(output_file, audio_data)

    except Exception as e:
        print(f"❌ TTS Error: {str(e)}")
        raise Exception(f"Gemini TTS failed: {str(e)}")
