from typing import Final

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# pip install gspread
import gspread

# google sheet API key and worksheet integration
sa = gspread.service_account(filename="service_account.json")
sh = sa.open("telegrambot")
wks = sh.worksheet("Sheet1")

print('Starting up bot...')
namedict={}
TOKEN: Final = '6223343604:AAEFmhEgzmKTEuQowDgX7LwBTpE92ajfHIM'
BOT_USERNAME: Final = '@testnitsri_bot'


"""async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaderboard = sorted(namedict.items(), key=lambda x: x[1], reverse=True)  # Sort the dictionary by streaks in descending order
    leaderboard_text = 'Leaderboard:\n'
    for index, (name, streak) in enumerate(leaderboard, start=1):
        leaderboard_text += f'{index}. {name}: {streak} days\n'
    await update.message.reply_text(leaderboard_text)"""




# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')




def handle_response(text: str,update) -> str:
    # Create your own response logic
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I\'m good thanks!'
    
    if 'leaderboard' in processed:
        leaderboard = sorted(namedict.items(), key=lambda x: x[1], reverse=True)
        leaderboard_text = 'Leaderboard:\n'
        for index, (name, streak) in enumerate(leaderboard, start=1):
            leaderboard_text += f'{index}. {name}: {streak} days\n'
        return leaderboard_text
    
    if 'i have completed' in processed:
        if update.message.from_user.first_name not in namedict:
            return f'{update.message.from_user.first_name}, you have not registered!'
        namedict[update.message.from_user.first_name]+=1
        return f'You are on a streak of {namedict[update.message.from_user.first_name]} days!'

    """if 'register' in processed:
        if update.message.from_user.first_name in namedict:
            return f'{update.message.from_user.first_name}, you have already registered!'
        namedict[update.message.from_user.first_name]=0      
        return f'{update.message.from_user.first_name}, you have successfully registered!'"""
    
    if 'register' in processed:
        
        for i in range(len(wks.get("B1:B70"))):
            if wks.get("B1:B70")[i][0]==update.message.from_user.first_name:
                return f'{update.message.from_user.first_name}, you have already registered!'
        wks.update_cell(len(wks.get("B1:B70"))+1, 2, update.message.from_user.first_name)
        return f'{update.message.from_user.first_name}, you have successfully registered!'
    





    return 'I don\'t understand'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.from_user.first_name}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text,update)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text,update)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('register', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
    


