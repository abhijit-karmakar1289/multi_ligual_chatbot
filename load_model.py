from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import os

# Default model: BLOOM
def load_bloom():
    print("🔹 Loading BLOOM model...")
    model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-1b7")
    tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-1b7")
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=2048,
        repetition_penalty=1.2,
        temperature=0.4
    )
    return pipe

# Optional model: DialoGPT
def load_dialogpt():
    print("🔹 Loading DialoGPT model...")
    model_name = "microsoft/DialoGPT-small"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=200
    )
    return pipe

# Select model based on environment variable or manually
MODEL_TYPE = os.getenv("CHAT_MODEL", "bloom") # "bloom" or "dialogpt"

if MODEL_TYPE == "dialogpt":
    pipe = load_dialogpt()
else:
    pipe = load_bloom()
