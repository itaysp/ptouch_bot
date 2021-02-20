#!/usr/bin/env python3

import print_consts
import logging
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from functools import wraps

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in print_consts.ALLOWED_USER_IDS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
@restricted
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    help_cmd = subprocess.check_output('ptouch-print',  '--info')
    update.message.reply_text(help_cmd)

@restricted
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

@restricted
def print_sticker(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    print_text = update.message.text.splitlines()
    update.message.reply_text("Printing\n\"" + update.message.text +"\"")
    cmd = ['ptouch-print', '--debug', '--pad', print_consts.PADDING , '--text'] + print_text
    print(cmd)
    subprocess.call(cmd)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=print_consts.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, print_sticker))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
