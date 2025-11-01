import torch
import soundfile as sf
import sounddevice as sd
from .model_loader import model, tokenizer, desc_tokenizer, device
import time
import uuid

# TTS Function using pre-loaded model
def synthesize_speech(text, discription, output_dir="Testing/audio_files"):
    desc_inputs= desc_tokenizer(discription,return_tensors="pt" )
    desc_inputs = {k: v.to(device) for k, v in desc_inputs.items()}

    prompt_inputs = tokenizer(text, return_tensors="pt")
    prompt_inputs = {k: v.to(device) for k, v in prompt_inputs.items()}

    with torch.no_grad():
        generation = model.generate(
            input_ids=desc_inputs["input_ids"],
            attention_mask=desc_inputs["attention_mask"],
            prompt_input_ids=prompt_inputs["input_ids"],
            prompt_attention_mask=prompt_inputs["attention_mask"],
            do_sample=True
        )

    audio_np = generation.cpu().numpy().squeeze().astype("float32")
    filename = f"{output_dir}/output_{uuid.uuid4().hex[:8]}.wav"
    sf.write(filename, audio_np, model.config.sampling_rate)
    return filename

# Call it

