from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Prompt template for grammar correction and translation
translation_prompt_template = """
You are a professional translator and grammar corrector.

Input text (in {source_lang}): {input_text}

Step 1: Correct any grammatical mistakes or ASR errors in the input text, keeping it natural and fluent in {source_lang}. This corrected version will be shown to the user.

Step 2: Translate the corrected text from {source_lang} to {target_lang}, ensuring the translation is accurate, natural, and fluent.

Output ONLY a valid JSON list with exactly two strings, no extra text:
["Corrected source text in {source_lang}", "Translated text in {target_lang}"]
"""

def translate_text(text, source_lang, target_lang):
    try:
        prompt = translation_prompt_template.format(
            input_text=text,
            source_lang=source_lang,
            target_lang=target_lang,
        )
        response_text = ""
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=True,
            stop=None
        )
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
        
        response_text = response_text.strip()
        print(f"Groq Response: {response_text}")
        result_list = json.loads(response_text)
        if not isinstance(result_list, list) or len(result_list) != 2:
            raise ValueError("Expected a list with 2 items")
        
        corrected_text = result_list[0]  # Index 0 = corrected
        translation = result_list[1]      # Index 1 = translation
        
        print("Translation response:", (corrected_text, translation))
        return corrected_text, translation
    
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {str(e)}")
        raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")
    except Exception as e:
        print(f"Translation Error: {str(e)}")
        raise Exception(f"Groq Translation failed: {str(e)}")
