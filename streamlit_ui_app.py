import streamlit as st
import asyncio
import time
import requests
import io
import os
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from STT.ASR import capture_and_transcribe_audio
from LLM.llm import translate_text
from TTS.gemini_tts import gemini_tts_synthesize


# Custom CSS for styling
# Custom CSS for styling - UPDATED
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8f0f7 100%) !important;
        color: #2c3e50 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    .header {
        color: #1a5f7a;
        text-align: center;
        padding: 15px 0;
        font-size: 2.2em;
        font-weight: 700;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    
    .card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border-radius: 12px;
        padding: 16px;
        margin: 5px 0;
        box-shadow: 0 4px 12px rgba(26, 95, 122, 0.1);
        border-left: 4px solid #1a5f7a;
        min-height: 180px;
        width: 100%;
    }
    
    .card h3 {
        color: #1a5f7a;
        font-size: 1.4em;
        margin-bottom: 12px;
        font-weight: 600;
    }
    
    .card h4 {
        color: #2c5aa0;
        font-size: 1.1em;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    
    .success { 
        color: #27ae60;
        font-weight: 600;
    }
    
    .warning { 
        color: #f39c12;
        font-weight: 600;
    }
    
    .error { 
        color: #e74c3c;
        font-weight: 600;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 2px solid #d1e3f0 !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        padding: 10px !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    .stTextArea textarea:focus {
        border: 2px solid #1a5f7a !important;
        box-shadow: 0 0 8px rgba(26, 95, 122, 0.2) !important;
    }
        /* FIXED: Text area styling with visible text */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 2px solid #d1e3f0 !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        padding: 10px !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-weight: 500 !important;
    }
    /* Force text area visibility */
    .stTextArea > div > div > textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Alternative selector */
    textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Debug: Make it obvious */
    .stTextArea {
        background-color: #ffffff !important;
    }
    .stTextArea textarea::placeholder {
        color: #999999 !important;
    }
    
    .stTextArea textarea:focus {
        border: 2px solid #1a5f7a !important;
        box-shadow: 0 0 8px rgba(26, 95, 122, 0.2) !important;
        color: #000000 !important;
    }
    
    /* Markdown text inside cards */
    .stMarkdown p {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }
    
    .stMarkdown strong {
        color: #1a5f7a !important;
        font-weight: 700 !important;
    }

    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1a5f7a 0%, #2c5aa0 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        margin-top: 10px;
        box-shadow: 0 4px 12px rgba(26, 95, 122, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(26, 95, 122, 0.4);
        background: linear-gradient(135deg, #0f4c5c 0%, #1a5f7a 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    .stButton > button:disabled {
        background: #bdc3c7;
        box-shadow: none;
        transform: none;
        cursor: not-allowed;
    }
    
    /* Markdown text styling */
    .stMarkdown {
        color: #2c3e50 !important;
    }
    
    .status-text {
        font-size: 0.95em;
        text-align: center;
        font-weight: 500;
        padding: 12px;
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%) !important;
    }
    
    .stSidebar > div > div:first-child {
        background: transparent !important;
    }
    
    .stSelectbox label {
        color: #1a5f7a !important;
        font-weight: 600 !important;
    }
    
    .stColumn > div {
        width: 100%;
        max-width: none;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'source_corrected' not in st.session_state:
    st.session_state.source_corrected = ""
if 'source_translation' not in st.session_state:
    st.session_state.source_translation = ""
if 'target_corrected' not in st.session_state:
    st.session_state.target_corrected = ""
if 'target_translation' not in st.session_state:
    st.session_state.target_translation = ""
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'source_lang' not in st.session_state:
    st.session_state.source_lang = "Telugu"
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "Tamil"


# Async Translation and TTS Pipeline
async def run_translation(input_lang, output_lang, is_source_to_target=True):
    """
    Async pipeline: ASR → Translation → TTS (Gemini + file-based playback)
    """
    status_area = st.empty()
    
    try:
        # Step 1: ASR Processing
        status_area.markdown(
            f'<div class="card status-text warning">🎤 Listening in {input_lang}... Speak now!</div>',
            unsafe_allow_html=True
        )
        start_time = time.time()
        transcription = await capture_and_transcribe_audio(input_lang)
        asr_time = time.time() - start_time
    
        if not transcription:
            status_area.markdown(
                '<div class="card status-text error">❌ No speech detected or transcription failed</div>',
                unsafe_allow_html=True
            )
            return
        
        # Step 2: Translation (LLM - returns both corrected_text and translation)
        status_area.markdown(
            f'<div class="card status-text">🌐 Translating...</div>',
            unsafe_allow_html=True
        )
        start_translate = time.time()
        
        # translate_text returns (corrected_source, translation)
        corrected_text, translated_text = translate_text(transcription, input_lang, output_lang)
        translate_time = time.time() - start_translate
        
        # Update session state based on direction
        if is_source_to_target:
            st.session_state.source_corrected = corrected_text
            st.session_state.source_translation = translated_text
        else:
            st.session_state.target_corrected = corrected_text
            st.session_state.target_translation = translated_text
        
        # Step 3: TTS Processing (Gemini TTS - returns file path)
        status_area.markdown(
            f'<div class="card status-text">🔊 Generating {output_lang} Speech...</div>',
            unsafe_allow_html=True
        )
        
        start_tts = time.time()
        
        try:
            audio_file_path = await gemini_tts_synthesize(translated_text)
            if audio_file_path and os.path.exists(audio_file_path):
                data, samplerate = sf.read(audio_file_path)
                sd.play(data, samplerate)
                sd.wait()  # Wait until playback finishes
                
                tts_time = time.time() - start_tts
                
                status_area.markdown(
                    f'<div class="card status-text success"> Completed! ASR: {asr_time:.2f}s, Translation: {translate_time:.2f}s, TTS: {tts_time:.2f}s</div>',
                    unsafe_allow_html=True
                )
            else:
                raise Exception(f"Audio file not found: {audio_file_path}")

        except Exception as tts_error:
            # Fallback to FastAPI TTS
            with status_area.container():
                st.warning(f"⚠️ Gemini TTS failed. Trying FastAPI fallback...")
            description = "Jaya speaks with a slightly high-pitched, quite monotone voice at a slightly faster-than-average pace in a confined space with very clear audio. The speaker speaks naturally. The recording is very high quality with no background noise."
            
            res = requests.post(
                "http://localhost:8000/synthesize",
                json={"text": translated_text, "description": description},
                timeout=10
            )
            
            if res.status_code == 200:
                audio_bytes = io.BytesIO(res.content)
                data, samplerate = sf.read(audio_bytes)
                sd.play(data, samplerate)
                sd.wait()
                
                tts_time = time.time() - start_tts
                status_area.markdown(
                    f'<div class="card status-text success">✅ FastAPI TTS Success! ASR: {asr_time:.2f}s, Translation: {translate_time:.2f}s, TTS: {tts_time:.2f}s</div>',
                    unsafe_allow_html=True
                )
            else:
                status_area.markdown(
                    f'<div class="card status-text error">❌ FastAPI TTS Error: {res.status_code} - {res.text}</div>',
                    unsafe_allow_html=True
                )
    
    except Exception as e:
        status_area.markdown(
            f'<div class="card status-text error">❌ Error: {str(e)}</div>',
            unsafe_allow_html=True
        )


# Streamlit UI
st.title("🎙️Vaani Anuvad: Speech-to-Speech Indic Translation System")
st.markdown(
    f"Supports 22 indan offical languages: Telugu, Tamil, Hindi, English, Bengali, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Urdu, Assamese",
    unsafe_allow_html=True
)


# Sidebar for language selection
with st.sidebar:
    st.title("⚙️ Language Settings")
    st.session_state.source_lang = st.selectbox(
        "Source Language",
        ["Telugu", "Tamil", "Hindi", "English", "Bengali", "Kannada", "Malayalam","Marathi", "Gujarati", "Punjabi", "Urdu","Assamese"],
        index=["Telugu", "Tamil", "Hindi", "English", "Bengali", "Kannada", "Malayalam","Marathi", "Gujarati", "Punjabi", "Urdu","Assamese"].index(st.session_state.source_lang)
    )
    st.session_state.target_lang = st.selectbox(
        "Target Language",
        ["Telugu", "Tamil", "Hindi", "English", "Bengali", "Kannada", "Malayalam","Marathi", "Gujarati", "Punjabi", "Urdu","Assamese"],
        index=["Telugu", "Tamil", "Hindi", "English", "Bengali", "Kannada", "Malayalam","Marathi", "Gujarati", "Punjabi", "Urdu","Assamese"].index(st.session_state.target_lang)
    )


st.markdown("""
<div class="card">
    <h4>How to use:</h4>
    <ol>
        <li>Supports 22 indan offical languages: Telugu, Tamil, Hindi, English, Bengali, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Urdu, Assamese</li>
        <li>Select source and target languages in the sidebar</li>
        <li>Click 'Speak {source_lang}' to:
            <ul>
                <li>Capture speech in {source_lang}</li>
                <li>Get corrected text in {source_lang}</li>
                <li>Get translation to {target_lang}</li>
                <li>Hear the {target_lang} translation</li>
            </ul>
        </li>
        <li>Click 'Speak {target_lang}' to do the reverse</li>
        <li>View both corrected text and translations in the respective cards</li>
    </ol>
</div>
""".format(source_lang=st.session_state.source_lang, target_lang=st.session_state.target_lang), unsafe_allow_html=True)


# Status indicator
if st.session_state.is_processing:
    st.markdown('<div class="card status-text">⏳ Processing... Please wait</div>', unsafe_allow_html=True)

# Two-column layout with cards
col1, col2 = st.columns(2)


with col1:
    st.markdown(f"<div class='card'><h3>🎙️ {st.session_state.source_lang}</h3>", unsafe_allow_html=True)
    
    st.markdown(f"**Orginal Language:**")
    st.markdown(f"""
    <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; border: 2px solid #1a5f7a; min-height: 90px; color: #000000; font-size: 16px; font-weight: 500;">
    {st.session_state.source_corrected if st.session_state.source_corrected else '<em style="color: #999;">Waiting for speech...</em>'}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Translation to {st.session_state.target_lang}:**")
    st.markdown(f"""
    <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; border: 2px solid #1a5f7a; min-height: 90px; color: #000000; font-size: 16px; font-weight: 500;">
    {st.session_state.source_translation if st.session_state.target_translation else '<em style="color: #999;">Translation will appear here...</em>'}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(
        f'⏺️ Speak {st.session_state.source_lang}', 
        key='source_btn', 
        use_container_width=True, 
        disabled=st.session_state.is_processing
    ):
        st.session_state.is_processing = True
        asyncio.run(run_translation(
            st.session_state.source_lang, 
            st.session_state.target_lang, 
            is_source_to_target=True
        ))
        st.session_state.is_processing = False
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


with col2:
    st.markdown(f"<div class='card'><h3>🌐 {st.session_state.target_lang}</h3>", unsafe_allow_html=True)
    st.markdown(f"**Original Language:**")
    st.markdown(f"""
    <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; border: 2px solid #1a5f7a; min-height: 90px; color: #000000; font-size: 16px; font-weight: 500;">
    {st.session_state.target_corrected if st.session_state.target_corrected else '<em style="color: #999;">Waiting for speech...</em>'}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Translation to {st.session_state.target_lang}:**")
    st.markdown(f"""
    <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; border: 2px solid #1a5f7a; min-height: 90px; color: #000000; font-size: 16px; font-weight: 500;">
    {st.session_state.target_translation if st.session_state.source_translation else '<em style="color: #999;">Translation will appear here...</em>'}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(
        f'⏺️ Speak {st.session_state.target_lang}', 
        key='target_btn', 
        use_container_width=True, 
        disabled=st.session_state.is_processing
    ):
        st.session_state.is_processing = True
        asyncio.run(run_translation(
            st.session_state.target_lang, 
            st.session_state.source_lang, 
            is_source_to_target=False
        ))
        st.session_state.is_processing = False
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


