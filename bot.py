import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random
from threading import Thread
from flask import Flask

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Truth questions
TRUTHS = [
    "What's the most embarrassing thing you've ever done?",
    "What's your biggest fear?",
    "Have you ever told a lie to get out of trouble?",
    "What's the worst gift you've ever received?",
    "Who was your first crush?",
    "What's something you've never told anyone?",
    "What's your most embarrassing childhood memory?",
    "Have you ever cheated on a test?",
    "What's the biggest lie you've ever told?",
    "What's your guilty pleasure?",
    "Who in this group do you trust the most?",
    "What's the most childish thing you still do?",
    "Have you ever stalked someone on social media?",
    "What's your biggest insecurity?",
    "What's the worst date you've ever been on?",
    "If you could swap lives with someone for a day, who would it be?",
    "What's the most trouble you've been in?",
    "Have you ever ghosted someone?",
    "What's your most unpopular opinion?",
    "What's the craziest dream you've ever had?",
    "What's the most embarrassing thing in your search history?",
    "Who was your worst kiss?",
    "What's your biggest regret?",
    "Have you ever pretended to be sick to skip something?",
    "What's the longest you've gone without showering?",
]

# Dare challenges
DARES = [
    "Do 20 push-ups right now and send proof!",
    "Send a funny selfie to the group.",
    "Speak in an accent for the next 3 messages.",
    "Do your best dance and describe it in detail.",
    "Send a voice message singing your favorite song.",
    "Change your group profile picture to something funny.",
    "Let the person above you write your status for 24 hours.",
    "Do 30 jumping jacks and send a video!",
    "Imitate another group member (describe in detail).",
    "Share your most embarrassing photo.",
    "Talk in rhymes for the next 5 messages.",
    "Do your best celebrity impression in text.",
    "Send a message to your crush (screenshot it!).",
    "Post a throwback photo from 5+ years ago.",
    "Let someone else choose your profile picture for a week.",
    "Write a funny poem about someone in the group.",
    "Share the last photo in your gallery.",
    "Do 50 jumping jacks.",
    "Share your screen time report.",
    "Send a meme that describes your life right now.",
    "Text your mom 'I love you' right now.",
    "Do 10 burpees and send proof.",
    "Share an embarrassing voice note.",
    "Let someone send a text from your phone.",
    "Post a story saying 'I lost a bet'.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat_type = update.effective_chat.type
    
    if chat_type == "private":
        welcome_message = (
            f"🎭 Welcome {user.mention_html()}!\n\n"
            "I'm your Truth or Dare bot!\n\n"
            "<b>Commands:</b>\n"
            "🤔 /truth - Get a truth question\n"
            "💪 /dare - Get a dare challenge\n"
            "❓ /help - Show help message\n\n"
            "💡 <b>Tip:</b> Add me to a group chat to play with friends!\n\n"
            "Let's have some fun! 🎉"
        )
    else:
        welcome_message = (
            f"🎭 Hello everyone! I'm the Truth or Dare bot!\n\n"
            "<b>How to play:</b>\n"
            "• Type /truth for a truth question\n"
            "• Type /dare for a dare challenge\n"
            "• Type /help for more info\n\n"
            "Ready to have some fun? 🎉"
        )
    
    await update.message.reply_html(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🎮 <b>How to Play:</b>\n\n"
        "<b>Commands:</b>\n"
        "🤔 /truth - Get a random truth question\n"
        "💪 /dare - Get a random dare challenge\n"
        "❓ /help - Show this help message\n\n"
        "<b>Group Play:</b>\n"
        "• Anyone can use /truth or /dare anytime\n"
        "• All messages stay in the chat for everyone to see\n"
        "• Take turns and have fun!\n"
        "• Be honest and brave! 💪\n\n"
        "<b>Private Play:</b>\n"
        "• Chat with me directly for solo games\n"
        "• Perfect for practicing!\n\n"
        "Enjoy! 🎉"
    )
    await update.message.reply_html(help_text)

async def truth_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random truth question."""
    user = update.effective_user
    truth = random.choice(TRUTHS)
    
    message = (
        f"🤔 <b>TRUTH for {user.mention_html()}:</b>\n\n"
        f"{truth}\n\n"
        f"💬 Answer honestly!"
    )
    
    await update.message.reply_html(message)

async def dare_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random dare challenge."""
    user = update.effective_user
    dare = random.choice(DARES)
    
    message = (
        f"💪 <b>DARE for {user.mention_html()}:</b>\n\n"
        f"{dare}\n\n"
        f"🔥 You got this!"
    )
    
    await update.message.reply_html(message)

# Flask web server to keep Render happy
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Truth or Dare Bot is running!"

@app.route('/health')
def health():
    return "OK"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def main() -> None:
    """Start the bot."""
    # Get token from environment variable (for cloud deployment) or use hardcoded token
    TOKEN = os.environ.get('BOT_TOKEN', '8099766090:AAH7-FarY-kZoP7PuEriLss3Fizq7NJQFbo')
    
    if TOKEN == 'YOUR_TOKEN_HERE':
        print("⚠️  WARNING: Please set your bot token!")
        print("For local testing, replace 'YOUR_TOKEN_HERE' in the code.")
        print("For cloud deployment, set the BOT_TOKEN environment variable.")
        return
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("truth", truth_command))
    application.add_handler(CommandHandler("dare", dare_command))
    
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start the Bot
    print("✅ Bot is running... Press Ctrl+C to stop.")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
