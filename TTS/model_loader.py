import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import warnings
import logging
from transformers.utils.logging import set_verbosity_error
import os

# Silence logs
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN

warnings.filterwarnings("ignore",message="Flash attention 2 is not installed")
set_verbosity_error()
logging.getLogger().setLevel(logging.ERROR)

# Device
device = torch.device("cuda:0")
dtype = torch.float16

# Load once and reuse
print(f"✅ Using GPU: {torch.cuda.get_device_name(0)}")
print("🔄 Loading TTS model...")
attn_implementation = "eager"
model = ParlerTTSForConditionalGeneration.from_pretrained("ai4bharat/indic-parler-tts",attn_implementation=attn_implementation).to(device,dtype=    dtype)
model.eval()  # Important for inference
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts")
desc_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)


print(f"Model loaded on: {next(model.parameters()).device} with dtype: {next(model.parameters()).dtype}")
# Expose to other modules
__all__ = ["model", "tokenizer", "desc_tokenizer", "device", "dtype"]

# TTS