# 🎙️ Vaani Anuvad: Speech-to-Speech Indic Translation System

**Seamlessly translate speech across all 22 Official Indian Languages in real-time**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit)](https://streamlit.io/)
[![Groq API](https://img.shields.io/badge/Groq-OpenAI%20120B-blueviolet)](https://console.groq.com/)
[![Gemini TTS](https://img.shields.io/badge/Google-Gemini%202.5-orange)](https://ai.google.dev/)

---

## 🎯 Overview

**Vaani Anuvad** ([translate:वाणी अनुवाद]) is an intelligent Speech-to-Speech translation system designed exclusively for Indian languages. It bridges communication gaps by enabling real-time, bidirectional speech translation across all **22 Official Indian Languages**.

Perfect for multilingual teams, businesses, educational institutions, and individuals who want to communicate without language barriers.

---

## ✨ Key Features

- 🎙️ **Real-Time Speech Translation** — Speak in one language, get instant translation in another
- 🌐 **22 Indian Languages Supported**:
  - [translate:తెలుగు] (Telugu) | [translate:தமிழ்] (Tamil) | [translate:हिंदी] (Hindi) | [translate:ಕನ್ನಡ] (Kannada)
  - [translate:മലയാളം] (Malayalam) | [translate:বাংলা] (Bengali) | [translate:ગુજરાતી] (Gujarati) | [translate:ਪੰਜਾਬੀ] (Punjabi)
  - [translate:मराठी] (Marathi) | [translate:ଓଡ଼ିଆ] (Odia) | [translate:അസ്സാമീസ്] (Assamese) | And 11 more...

- 🧠 **Grammar Correction & Translation** — Powered by **Groq API (OpenAI 120B Model)**
  - Corrects ASR errors automatically
  - Provides natural, fluent translations
  - Context-aware processing

- 🔊 **Dual TTS Engines**:
  - **Primary**: Google Gemini Flash 2.5 TTS (high-quality, natural voices)
  - **Fallback**: AI4Bharat Indic-Parler TTS (supports all 22 Indian languages reliably)

- ⚡ **Advanced ASR** — Whisper-based speech recognition with language detection
- 📝 **Dual Display** — See both corrected text and translation simultaneously
- 🎨 **Beautiful UI** — Professional Streamlit interface with real-time status
- ⚙️ **Production Ready** — FastAPI backend with async support & error handling

---

## 🎬 Demo Videos

### Watch Vaani Anuvad in Action 

#### Demo 1: [translate:తెలుగు] (Telugu) to  (Kannada)

[Watch Video](Video_demo\streamlit_ui_demo.mp4)


---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit 1.28+ | Interactive chat UI with real-time display |
| **ASR** | OpenAI Whisper | Speech-to-text recognition |
| **LLM** | Groq API (OpenAI 120B) | Grammar correction & translation |
| **Primary TTS** | Google Gemini 2.5 Flash | Natural speech synthesis |
| **Fallback TTS** | AI4Bharat Indic-Parler | Comprehensive Indian language support |
| **Backend** | FastAPI + Uvicorn | API server with async processing |
| **Audio Processing** | soundfile + sounddevice | Real-time audio playback |
| **Async Framework** | asyncio | Non-blocking pipeline |

---

## 🚀 4. Quick Start

### ⚙️ System Requirements
- 💻 **Recommended RAM:** 4GB+  
- 🧠 **GPU (Optional but Recommended):**  

### 📦 Setup & Run
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/sreenivas1440/VaaniAnuvad.git
   cd   VaaniAnuvad
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Secrets** (create `.env`):
   ```env
   Groq_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_gemini_key_here
   ```

4. **Launch the App**:
   ```bash
   streamlit run streamlit_ui_app.py
   ```
   Open [http://localhost:8501](http://localhost:8501) – query away! 🎉
   
---

## 🔧 FastAPI Backend Setup (Recommended for Production)

### ⚡ Why Use FastAPI Backend?

The **AI4Bharat Indic-Parler TTS** model (900M parameters) is resource-intensive:
- 🚨 **Without backend**: Model loads to GPU/RAM on **every request** → High latency (5-8s)
- ✅ **With backend**: Model loads **once** at startup → Sub-2s latency per request

### 📋 System Requirements for FastAPI

- **GPU**: NVIDIA GPU with 4GB+ VRAM (RTX 3060, A10, L4, etc.) **STRONGLY RECOMMENDED**
- **CPU-only**: Possible but slow (10-15s per request)
- **RAM**: 8GB+ recommended
- **CUDA**: 11.8+ (if using GPU)

### 🚀 Launch FastAPI Backend

#### **Option 1: GPU-Accelerated (Recommended)**

1. **Install GPU dependencies** (if not already installed):
    ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
2. **Start FastAPI server**:
   ```bash
   uvicorn TTS.main:app --reload
   ```

#### **Option 2: CPU-Only**   uvicorn TTS.main:app



## 📁 Project Structure
```
    Vaani-Anuvad/
    ├── 📁 LLM/ # Language Model & Translation
    │ ├── init.py
    │ └── llm.py # Groq API integration
    │
    │
    ├── 📁 STT/ # Speech-to-Text
    │ ├── init.py
    │ └── ASR.py # Whisper ASR
    │ 
    ├── 📁 TTS/ # Text-to-Speech
    │ ├── init.py
    │ ├── main.py # FastAPI backend server
    │ ├── gemini_tts.py # Google Gemini TTS
    │ ├── tts.py # Indic-Parler TTS wrapper
    │ ├── model_loader.py # Model loading utilities
    │ └── play.py # Audio playback
    │ 
    │
    ├── 📁 Testing/ # Testing & Audio Files
    │ └── 📁 audio_files/ # Generated audio storage
    │ ├── tts_2025_11_01_...wav # Output audio files
    │ ├── tts_2025_11_01_...wav
    │ └── ...
    ├── 📄 README.md # Project documentation
    ├── 📄 requirements.txt # Python dependencies
    ├── 📄 .env.example # Environment variables template
    ├── 📄 .gitignore # Git ignore rules
    ├── 📄 LICENSE # MIT License
    │
    ├── 📱 streamlit_ui_app.py # Main Streamlit application
```
   
## 🎯 Supported Languages

| Language | Code | Native Name | Example |
|----------|------|-------------|---------|
| Telugu | te | [translate:తెలుగు] | [translate:నమస్కారం] |
| Tamil | ta | [translate:தமிழ்] | [translate:வணக்கம்] |
| Hindi | hi | [translate:हिंदी] | [translate:नमस्ते] |
| Kannada | kn | [translate:ಕನ್ನಡ] | [translate:ನಮಸ್ಕಾರ] |
| Malayalam | ml | [translate:മലയാളം] | [translate:നമസ്കാരം] |
| Bengali | bn | [translate:বাংলা] | [translate:নমস্কার] |
| Gujarati | gu | [translate:ગુજરાતી] | [translate:નમસ્તે] |
| Punjabi | pa | [translate:ਪੰਜਾਬੀ] | [translate:ਨਮਸਤੇ] |
| Marathi | mr | [translate:मराठी] | [translate:नमस्कार] |
| Odia | or | [translate:ଓଡ଼ିଆ] | [translate:ନମସ୍କାର] |
| + 12 more | ... | ... | ... |

---


---

## 🙏 Acknowledgments

- **ASR**: [OpenAI Whisper](https://github.com/openai/whisper)
- **LLM**: [Groq](https://www.groq.com/) & [OpenAI](https://openai.com/)
- **TTS**: [Google Gemini](https://ai.google.dev/) & [AI4Bharat](https://github.com/AI4Bharat/)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👨‍💻 Author
- GitHub: [sreenivas1440](https://github.com/sreenivas1440)

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 🌟 Show Your Support

Give this project a ⭐ if it helped you communicate across Indian languages!

---

**Built with ❤️ for bridging Indian languages through speech**

🎙️ **Vaani Anuvad** - One Voice, Many Languages
