import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Load API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Your Telegram bot token
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Your OpenAI API key

if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ ERROR: TELEGRAM_BOT_TOKEN or OPENAI_API_KEY is missing!")

# ✅ Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# ✅ Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ✅ Function to get response from ChatGPT
async def chatgpt_response(message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[{"role": "user", "content": message}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"🔥 OpenAI API Error: {e}")
        return "❌ Sorry, I couldn't process your request."

# ✅ Handler for the `/start` command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🤖 Hello! I am your ChatGPT bot. Ask me anything!")

# ✅ Handler for normal messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    bot_response = await chatgpt_response(user_message)
    await update.message.reply_text(bot_response)

# ✅ Main function to start the bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logging.info("🚀 Bot is running...")
    app.run_polling()

# ✅ FIXED: Correct `if __name__ == "__main__":` block
if __name__ == "__main__":
    main()
