import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

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
            "/play - Start playing Truth or Dare\n"
            "/help - Show help message\n\n"
            "💡 <b>Tip:</b> Add me to a group chat to play with friends!\n\n"
            "Let's have some fun! 🎉"
        )
    else:
        welcome_message = (
            f"🎭 Hello everyone! I'm the Truth or Dare bot!\n\n"
            "<b>Commands:</b>\n"
            "/play - Start a game\n"
            "/help - Show help\n\n"
            "Ready to have some fun? Type /play to begin! 🎉"
        )
    
    await update.message.reply_html(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🎮 <b>How to Play:</b>\n\n"
        "1. Use /play to start the game\n"
        "2. Choose Truth or Dare using the buttons\n"
        "3. Complete your challenge!\n"
        "4. Click 'Play Again' or use /play for another round\n\n"
        "<b>Group Play:</b>\n"
        "• Anyone can start a game with /play\n"
        "• Take turns choosing Truth or Dare\n"
        "• Have fun and be brave! 💪\n\n"
        "<b>Private Play:</b>\n"
        "• Chat with me directly for solo games\n"
        "• Perfect for practicing before group games!\n\n"
        "Enjoy! 🎉"
    )
    await update.message.reply_html(help_text)

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show Truth or Dare buttons."""
    keyboard = [
        [
            InlineKeyboardButton("🤔 Truth", callback_data='truth'),
            InlineKeyboardButton("💪 Dare", callback_data='dare')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    chat_type = update.effective_chat.type
    if chat_type == "private":
        message = '🎭 Choose wisely...\n\n<b>Truth or Dare?</b>'
    else:
        user = update.effective_user.first_name
        message = f'🎭 {user} wants to play!\n\n<b>Truth or Dare?</b>'
    
    await update.message.reply_html(message, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user.first_name
    
    if query.data == 'truth':
        truth = random.choice(TRUTHS)
        message = f"🤔 <b>TRUTH for {user}:</b>\n\n{truth}\n\n💬 Answer honestly!"
    elif query.data == 'dare':
        dare = random.choice(DARES)
        message = f"💪 <b>DARE for {user}:</b>\n\n{dare}\n\n🔥 You got this!"
    elif query.data == 'play_again':
        keyboard = [
            [
                InlineKeyboardButton("🤔 Truth", callback_data='truth'),
                InlineKeyboardButton("💪 Dare", callback_data='dare')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f'🎭 {user} is playing!\n\n<b>Truth or Dare?</b>',
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        return
    
    # Add play again button
    keyboard = [[InlineKeyboardButton("🔄 Play Again", callback_data='play_again')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode='HTML')

def main() -> None:
    """Start the bot."""
    # Get token from environment variable (for cloud deployment) or use hardcoded token
    TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_TOKEN_HERE')
    
    if TOKEN == '8099766090:AAH7-FarY-kZoP7PuEriLss3Fizq7NJQFbo':
        print("⚠️  WARNING: Please set your bot token!")
        print("For local testing, replace 'YOUR_TOKEN_HERE' in the code.")
        print("For cloud deployment, set the BOT_TOKEN environment variable.")
        return
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("play", play))
    
    # Register callback handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start the Bot
    print("✅ Bot is running... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
