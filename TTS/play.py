import requests
import soundfile as sf
import sounddevice as sd
text = input("Enter the text: :")
description = "Jaya speaks with a slightly high-pitched, quite monotone voice at a slightly faster-than-average pace in a confined space with very clear audio. The speaker speaks naturally. The recording is very high quality with no background noise."
# Send POST request to FastAPI
res = requests.post(
    "http://localhost:8000/synthesize",
    json={"text": text, "description":description})

if res.status_code != 200:
    print("Error:", res.status_code, res.text)
    exit()
# Save and play response audio
with open("response.wav", "wb") as f:
    f.write(res.content)

data, samplerate = sf.read("response.wav")
sd.play(data, samplerate)
sd.wait()
 