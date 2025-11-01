from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from TTS.tts import synthesize_speech  # ✅ your speech generation function
import time
app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    description: str = (
        "Jaya speaks with a slightly high-pitched, quite monotone voice at a slightly faster-than-average pace in a confined space with very clear audio. The speaker speaks naturally. The recording is very high quality with no background noise."
    )
  
@app.post("/synthesize")
async def synthesize(req: TTSRequest):
    try:
        output_file = synthesize_speech(req.text, req.description)
        return FileResponse( 
            output_file,
            media_type="audio/wav",
            filename=output_file.split("/")[-1]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
