import gradio as gr
from load_model import pipe
from utils import Translation
from deep_translator import GoogleTranslator
import json
import os

# Supported languages
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Bengali": "bn",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Arabic": "ar"
}

USER_DB_FILE = "user_db.json"

# Load user db from json file
def load_user_db():
    if not os.path.exists(USER_DB_FILE):
        default_users = {"user1": "pass1", "user2": "pass2"}
        with open(USER_DB_FILE, "w") as f:
            json.dump(default_users, f)
        return default_users
    with open(USER_DB_FILE, "r") as f:
        return json.load(f)

def save_user_db(user_db):
    with open(USER_DB_FILE, "w") as f:
        json.dump(user_db, f)

user_db = load_user_db()

def register_user(username, password):
    if username in user_db:
        return "Username already exists. Please choose another."
    if not username or not password:
        return "Username and password cannot be empty."
    user_db[username] = password
    save_user_db(user_db)
    return "Registration successful! Please login with your new credentials."

def login_user(username, password):
    return user_db.get(username) == password

def reply(message, output_lang_name):
    if not message.strip():
        return "Please type a message!"
    txt = Translation(message, "en")
    message_en = message if txt.original == "en" else txt.translatef()
    response = pipe(message_en)
    response_text_en = response[0]["generated_text"]
    output_lang_code = LANGUAGES.get(output_lang_name, "en")
    if output_lang_code != "en":
        try:
            response_text = GoogleTranslator(source="en", target=output_lang_code).translate(response_text_en)
        except Exception as e:
            response_text = f"[Translation Error] Returning English output.\n{response_text_en}"
    else:
        response_text = response_text_en
    return response_text

with gr.Blocks() as demo:
    login_panel = gr.Column(visible=True)
    register_panel = gr.Column(visible=False)
    chat_panel = gr.Column(visible=False)

    # Login UI
    with login_panel:
        gr.Markdown("### Login")
        login_username = gr.Textbox(label="Username")
        login_password = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")
        login_msg = gr.Textbox(label="", interactive=False)
        register_switch = gr.Button("New Registration")

    # Registration UI
    with register_panel:
        gr.Markdown("### Register")
        reg_username = gr.Textbox(label="Username")
        reg_password = gr.Textbox(label="Password", type="password")
        reg_button = gr.Button("Register")
        reg_msg = gr.Textbox(label="", interactive=False)
        back_button = gr.Button("Back to Login")

    # Chat UI - now with 'Submit' button
    with chat_panel:
        user_message = gr.Textbox(lines=2, placeholder="Type your message here...", label="Your Message")
        lang_choice = gr.Dropdown(list(LANGUAGES.keys()), label="Output Language", value="English")
        submit_btn = gr.Button("Submit")
        chat_response = gr.Textbox(label="Bot Response")

    # Interactivity functions
    def handle_login(username, password):
        ok = login_user(username, password)
        if ok:
            return "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)
        else:
            return "Invalid username or password.", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    def handle_register_open():
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    def handle_register(username, password):
        msg = register_user(username, password)
        show_login = msg.startswith("Registration successful")
        return msg, gr.update(visible=not show_login), gr.update(visible=show_login)
    def handle_back_to_login():
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    def handle_chat(message, lang):
        return reply(message, lang)

    # Button actions
    login_button.click(handle_login, [login_username, login_password], [login_msg, login_panel, register_panel, chat_panel])
    register_switch.click(handle_register_open, [], [login_panel, register_panel, chat_panel])
    reg_button.click(handle_register, [reg_username, reg_password], [reg_msg, register_panel, login_panel])
    back_button.click(handle_back_to_login, [], [login_panel, register_panel, chat_panel])
    submit_btn.click(handle_chat, [user_message, lang_choice], chat_response)
    user_message.submit(handle_chat, [user_message, lang_choice], chat_response)

demo.launch()
