import os
from huggingface_hub import login

def hf_login():
    HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not HF_TOKEN:
        raise ValueError("❌ Please set HUGGINGFACE_HUB_TOKEN environment variable!")
    try:
        login(token=HF_TOKEN, add_to_git_credential=False)
        print("✅ Successfully authenticated with Hugging Face")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
