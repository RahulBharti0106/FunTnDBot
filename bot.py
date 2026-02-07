import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random
from threading import Thread
from flask import Flask
from data import TRUTHS, DARES, WOULD_YOU_RATHER, ROASTS, FATES


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat_type = update.effective_chat.type

    if chat_type == "private":
        welcome_message = (
            f"🎭 Welcome {user.mention_html()}!\n\n"
            "I'm your Truth or Dare bot with extra fun features!\n\n"
            "<b>Commands:</b>\n"
            "🎮 /play - Start playing with buttons\n"
            "🤔 /truth - Get a truth question\n"
            "💪 /dare - Get a dare challenge\n"
            "🤔💭 /wyr - Would you rather\n"
            "🔥 /roast - Get roasted\n"
            "🔮 /fate - Your fate prediction\n"
            "❓ /help - Show help message\n\n"
            "💡 <b>Tip:</b> Add me to a group chat to play with friends!\n\n"
            "Let's have some fun! 🎉"
        )
        await update.message.reply_html(welcome_message)
    else:
        welcome_message = (
            f"🎭 Hello everyone! I'm the Truth or Dare bot!\n\n"
            "<b>How to play:</b>\n"
            "• Type /truth for a truth question\n"
            "• Type /dare for a dare challenge\n"
            "• Type /wyr for would you rather\n"
            "• Type /roast to get roasted\n"
            "• Type /fate for your fate prediction\n"
            "• Type /help for more info\n\n"
            "Ready to have some fun? 🎉"
        )
        await update.message.reply_html(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    chat_type = update.effective_chat.type

    if chat_type == "private":
        help_text = (
            "🎮 <b>How to Play (Private Chat):</b>\n\n"
            "<b>Button Mode:</b>\n"
            "🎮 /play - Start with interactive buttons\n\n"
            "<b>Direct Commands:</b>\n"
            "🤔 /truth - Get a random truth question\n"
            "💪 /dare - Get a random dare challenge\n"
            "🤔💭 /wyr - Would you rather question\n"
            "🔥 /roast - Get roasted by the bot\n"
            "🔮 /fate - Get your fate prediction\n"
            "❓ /help - Show this help message\n\n"
            "💡 <b>Tip:</b> Use /play for easy button navigation!\n\n"
            "Enjoy! 🎉"
        )
    else:
        help_text = (
            "🎮 <b>How to Play (Group Chat):</b>\n\n"
            "<b>Commands:</b>\n"
            "🤔 /truth - Get a random truth question\n"
            "💪 /dare - Get a random dare challenge\n"
            "🤔💭 /wyr - Would you rather question\n"
            "🔥 /roast - Get roasted by the bot\n"
            "🔮 /fate - Get your fate prediction\n"
            "❓ /help - Show this help message\n\n"
            "<b>Group Play:</b>\n"
            # "• Anyone can use any command anytime\n"
            # "• All messages stay in the chat for everyone to see\n"
            "• Take turns and have fun!\n"
            "• Be honest and brave! 💪\n\n"
            "Enjoy! 🎉"
        )

    await update.message.reply_html(help_text)


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show game buttons - only works in private chat."""
    chat_type = update.effective_chat.type

    if chat_type != "private":
        await update.message.reply_text(
            "🎮 Button mode only works in private chat!\n\n"
            "In groups, use commands directly:\n"
            "/truth, /dare, /wyr, /roast, /fate"
        )
        return

    keyboard = [
        [
            InlineKeyboardButton("🤔 Truth", callback_data="truth"),
            InlineKeyboardButton("💪 Dare", callback_data="dare"),
        ],
        [InlineKeyboardButton("🤔💭 Would You Rather", callback_data="wyr")],
        [
            InlineKeyboardButton("🔥 Roast Me", callback_data="roast"),
            InlineKeyboardButton("🔮 My Fate", callback_data="fate"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎭 <b>Choose Your Game!</b>\n\nPick what you want to play:",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )


async def truth_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random truth question."""
    user = update.effective_user
    truth = random.choice(TRUTHS)

    message = (
        f"🤔 <b>TRUTH for {user.mention_html()}:</b>\n\n"
        f"{truth}\n\n"
        # f"💬 Answer honestly!"
    )

    await update.message.reply_html(message)


async def dare_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random dare challenge."""
    user = update.effective_user
    dare = random.choice(DARES)

    message = (
        f"💪 <b>DARE for {user.mention_html()}:</b>\n\n"
        f"{dare}\n\n"
        # f"🔥 You got this!"
    )

    await update.message.reply_html(message)


async def wyr_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random would you rather question."""
    user = update.effective_user
    wyr = random.choice(WOULD_YOU_RATHER)

    message = (
        f"🤔💭 <b>WOULD YOU RATHER for {user.mention_html()}:</b>\n\n"
        f"{wyr}\n\n"
        # f"🤷 Choose wisely!"
    )

    await update.message.reply_html(message)


async def roast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roast a user with savage but funny burns."""
    user = update.effective_user
    roast = random.choice(ROASTS)

    message = (
        f"🔥 <b>ROAST for {user.mention_html()}:</b>\n\n"
        f"{roast}\n\n"
        # f"😏 Just kidding... or am I?"
    )

    await update.message.reply_html(message)


async def fate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Predict someone's fate with humor."""
    user = update.effective_user
    fate = random.choice(FATES)

    message = (
        f"🔮 <b>FATE PREDICTION for {user.mention_html()}:</b>\n\n"
        f"{fate}\n\n"
        # f"✨ The universe has spoken!"
    )

    await update.message.reply_html(message)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses - creates NEW messages instead of editing."""
    query = update.callback_query
    await query.answer()

    user = query.from_user

    # Prepare the play again button
    keyboard = [
        [
            InlineKeyboardButton("🤔 Truth", callback_data="truth"),
            InlineKeyboardButton("💪 Dare", callback_data="dare"),
        ],
        [InlineKeyboardButton("🤔💭 Would You Rather", callback_data="wyr")],
        [
            InlineKeyboardButton("🔥 Roast Me", callback_data="roast"),
            InlineKeyboardButton("🔮 My Fate", callback_data="fate"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Generate response based on button pressed
    if query.data == "truth":
        truth = random.choice(TRUTHS)
        message = (
            f"🤔 <b>TRUTH:</b>\n\n"
            f"{truth}\n\n"
            # f"💬 Answer honestly!"
        )
    elif query.data == "dare":
        dare = random.choice(DARES)
        message = (
            f"💪 <b>DARE:</b>\n\n"
            f"{dare}\n\n"
            # f"🔥 You got this!"
        )
    elif query.data == "wyr":
        wyr = random.choice(WOULD_YOU_RATHER)
        message = (
            f"🤔💭 <b>WOULD YOU RATHER:</b>\n\n"
            f"{wyr}\n\n"
            # f"🤷 Choose wisely!"
        )
    elif query.data == "roast":
        roast = random.choice(ROASTS)
        message = (
            f"🔥 <b>ROAST:</b>\n\n"
            f"{roast}\n\n"
            # f"😏 Just kidding... or am I?"
        )
    elif query.data == "fate":
        fate = random.choice(FATES)
        message = (
            f"🔮 <b>FATE PREDICTION:</b>\n\n"
            f"{fate}\n\n"
            # f"✨ The universe has spoken!"
        )
    else:
        message = "Something went wrong! Try again."

    # Send a NEW message with the result and play again buttons
    await query.message.reply_html(message, reply_markup=reply_markup)


# Flask web server to keep Render happy
app = Flask(__name__)


@app.route("/")
def home():
    return "✅ Truth or Dare Bot is running!"


@app.route("/health")
def health():
    return "OK"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


def main() -> None:
    """Start the bot."""
    TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")

    if TOKEN == "YOUR_TOKEN_HERE":
        print("⚠️  WARNING: Please set your bot token!")
        print("For local testing, replace 'YOUR_TOKEN_HERE' in the code.")
        print("For cloud deployment, set the BOT_TOKEN environment variable.")
        return

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("play", play_command))
    application.add_handler(CommandHandler("truth", truth_command))
    application.add_handler(CommandHandler("dare", dare_command))
    application.add_handler(CommandHandler("wyr", wyr_command))
    application.add_handler(CommandHandler("roast", roast_command))
    application.add_handler(CommandHandler("fate", fate_command))

    # Register callback handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the Bot
    print("✅ Bot is running... Press Ctrl+C to stop.")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
