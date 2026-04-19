from langchain.tools import tool
import requests

from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

@tool
def send_message_to_telegram_bot(html):
    """send message to Telegram Bot 'Seek Bot'"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": html,
        "parse_mode": "HTML"
    }

    result = requests.post(url, json=payload).json()
    if result["ok"]:
        return  "Message sent successfully"
    else:
        return "Error sending message, " + result["description"]

if __name__ == "__main__":
    response = send_message_to_telegram_bot("hello, find a new cat!")
    print(response)