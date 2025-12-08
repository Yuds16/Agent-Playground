from google.adk.agents.llm_agent import Agent

from os import getenv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from telegram import Bot

TELEGRAM_TOKEN = getenv("TELEGRAM_BOT_TOKEN", "")

app = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(chat_id: str, message: str) -> dict:
    """Sends a message to a specified Telegram chat.

    Args:
        chat_id (str): The Telegram chat ID to which the message will be sent.
        message (str): The message content to be sent.

    Returns:
        dict: status and result or error msg.
    """
    try:
        response = app.send_message(chat_id=chat_id, text=message)
        return {"status": "success", "result": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
def read_telegram_messages():
    """Reads messages from the Telegram bot.

    Returns:
        list: A list of messages received by the bot.
    """
    try:
        updates = app.get_updates()
        messages = [update.message.to_dict() for update in updates if update.message]
        return {"status": "success", "messages": messages}
    except Exception as e:
        return {"status": "error", "message": str(e)}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='TeleAgent',
    description='A helpful assistant for user questions.',
    instruction='Interact with the user mainly through Telegram messages.',
    tools=[send_telegram_message, read_telegram_messages],
)
