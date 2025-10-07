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

# Would You Rather questions
WOULD_YOU_RATHER = [
    "Would you rather fight 100 duck-sized horses or 1 horse-sized duck?",
    "Would you rather always have to sing instead of speak or dance everywhere you go?",
    "Would you rather have a rewind button or a pause button for your life?",
    "Would you rather be able to talk to animals or speak all human languages?",
    "Would you rather have unlimited bacon but no more games, or unlimited games but no more bacon?",
    "Would you rather sweat mayo or have your armpits smell like onions?",
    "Would you rather have a mullet for a year or be bald for 6 months?",
    "Would you rather always have to enter rooms backwards or always have to somersault out?",
    "Would you rather have fingers as long as your legs or legs as short as your fingers?",
    "Would you rather fight Mike Tyson once or talk like him forever?",
    "Would you rather lose all your teeth or lose all your hair?",
    "Would you rather have a third nipple or an extra toe?",
    "Would you rather always wear wet socks or always have a small rock in your shoe?",
    "Would you rather have to sneeze but not be able to, or have something stuck in your eye for an entire year?",
    "Would you rather be forced to dance every time you hear music or be forced to sing along to any song you hear?",
    "Would you rather have a permanently clogged nose or a piece of green spinach stuck in your teeth forever?",
    "Would you rather communicate only in emojis or never be able to use emojis again?",
    "Would you rather have your browser history made public or your bank balance displayed on your forehead?",
    "Would you rather always have to say everything on your mind or never speak again?",
    "Would you rather eat a raw onion or a raw potato?",
    "Would you rather have your thoughts appear in text bubbles above your head or have everything you think come true?",
    "Would you rather be itchy for the rest of your life or sticky for the rest of your life?",
    "Would you rather have Cheetos dust on your fingers forever or have a popcorn kernel stuck in your teeth forever?",
    "Would you rather speak in rhymes for the rest of your life or only be able to speak in questions?",
    "Would you rather have to wear clown shoes every day or a clown wig every day?",
]

# Roasts
ROASTS = [
    "You're not stupid, you just have bad luck when thinking.",
    "I'd agree with you, but then we'd both be wrong.",
    "You're like a software update. Whenever I see you, I think 'not now.'",
    "If laughter is the best medicine, your face must be curing the world.",
    "You're the reason the gene pool needs a lifeguard.",
    "I'm not saying you're dumb, but you've got the survival instincts of a dodo bird.",
    "You bring everyone so much joy... when you leave the room.",
    "Your secrets are safe with me. I wasn't even listening.",
    "You're not the dumbest person in the world, but you better hope they don't die.",
    "I'd challenge you to a battle of wits, but I see you came unarmed.",
    "You're like a cloud. When you disappear, it's a beautiful day.",
    "I'm jealous of people who haven't met you yet.",
    "You're proof that evolution can go in reverse.",
    "If you were any more inbred, you'd be a sandwich.",
    "You're the human version of a participation trophy.",
    "Somewhere out there is a tree tirelessly producing oxygen for you. Go apologize to it.",
    "You're like Monday mornings - nobody likes you.",
    "I'd give you a nasty look, but you've already got one.",
    "You're not lazy, you're just on energy-saving mode... permanently.",
    "You have the perfect face for radio.",
    "If brains were dynamite, you wouldn't have enough to blow your nose.",
    "You're the reason God created the middle finger.",
    "I'd roast you, but my mom says I'm not allowed to burn trash.",
    "You're like a plunger - you bring up old crap that nobody wants to see.",
    "I would ask how old you are, but I know you can't count that high.",
    "You're so fake, even China denied making you.",
    "I'm not insulting you, I'm just describing you.",
    "You're the reason why shampoo has instructions.",
    "If I had a face like yours, I'd sue my parents.",
    "You're about as useful as a screen door on a submarine.",
]

# Fate Predictions
FATES = [
    "Your future holds... absolutely nothing impressive. But hey, at least you tried!",
    "You will find true love... right after you stop looking in the mirror so much.",
    "A great opportunity awaits you... to embarrass yourself in public. Again.",
    "Your destiny is to become legendary... at procrastination.",
    "Fortune favors the bold. Unfortunately, you're not bold, just loud.",
    "You will soon receive unexpected money... which you'll immediately waste on something stupid.",
    "A mysterious stranger will change your life... by blocking you on social media.",
    "Your dreams will come true... but only the embarrassing ones.",
    "Success is in your future... if you redefine what 'success' means.",
    "You will live a long and happy life... in your imagination.",
    "A big change is coming... you'll finally update your profile picture from 2015.",
    "Your destiny is to inspire others... to not be like you.",
    "The stars say you'll find wisdom... but they're probably talking about someone else.",
    "Great wealth is in your future... in Monopoly money.",
    "You will travel the world... via Google Maps street view.",
    "Your future is bright... unlike your decision-making skills.",
    "A surprise awaits you... it's the consequences of your actions.",
    "You will achieve greatness... at being average.",
    "The universe has big plans for you... mostly as a cautionary tale.",
    "Your fate is sealed... with duct tape and bad choices.",
    "You will meet your soulmate... they'll reject you, but you'll meet them!",
    "Success will knock on your door... but you'll be in the bathroom and miss it.",
    "Your future holds adventure... like finding a good parking spot.",
    "You will be remembered... for that one embarrassing thing you did.",
    "Destiny awaits... it's just stuck in traffic right now.",
    "The cosmos predict... you'll spend way too much time on your phone today.",
    "Your fortune says... you'll find something you lost. It was in your hand the whole time.",
    "A prophecy foretold... you'll accidentally like someone's old post while stalking them.",
    "The stars align to reveal... you'll eat way more pizza than you planned.",
    "Your destiny is written... in autocorrect fails and typos.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat_type = update.effective_chat.type
    
    if chat_type == "private":
        welcome_message = (
            f"🎭 Welcome {user.mention_html()}!\n\n"
            "I'm your Truth or Dare bot with extra fun features!\n\n"
            "<b>Commands:</b>\n"
            "🤔 /truth - Get a truth question\n"
            "💪 /dare - Get a dare challenge\n"
            "🤔💭 /wyr - Would you rather\n"
            "🔥 /roast - Get roasted\n"
            "🔮 /fate - Your fate prediction\n"
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
            "• Type /wyr for would you rather\n"
            "• Type /roast to get roasted\n"
            "• Type /fate for your fate prediction\n"
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
        "🤔💭 /wyr - Would you rather question\n"
        "🔥 /roast - Get roasted by the bot\n"
        "🔮 /fate - Get your fate prediction\n"
        "❓ /help - Show this help message\n\n"
        "<b>Group Play:</b>\n"
        "• Anyone can use any command anytime\n"
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

async def wyr_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random would you rather question."""
    user = update.effective_user
    wyr = random.choice(WOULD_YOU_RATHER)
    
    message = (
        f"🤔💭 <b>WOULD YOU RATHER for {user.mention_html()}:</b>\n\n"
        f"{wyr}\n\n"
        f"🤷 Choose wisely!"
    )
    
    await update.message.reply_html(message)

async def roast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roast a user with savage but funny burns."""
    user = update.effective_user
    roast = random.choice(ROASTS)
    
    message = (
        f"🔥 <b>ROAST for {user.mention_html()}:</b>\n\n"
        f"{roast}\n\n"
        f"😏 Just kidding... or am I?"
    )
    
    await update.message.reply_html(message)

async def fate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Predict someone's fate with humor."""
    user = update.effective_user
    fate = random.choice(FATES)
    
    message = (
        f"🔮 <b>FATE PREDICTION for {user.mention_html()}:</b>\n\n"
        f"{fate}\n\n"
        f"✨ The universe has spoken!"
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
    TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_TOKEN_HERE')
    
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
    application.add_handler(CommandHandler("wyr", wyr_command))
    application.add_handler(CommandHandler("roast", roast_command))
    application.add_handler(CommandHandler("fate", fate_command))
    
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start the Bot
    print("✅ Bot is running... Press Ctrl+C to stop.")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
