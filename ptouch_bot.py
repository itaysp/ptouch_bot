#!/usr/bin/env python3

import asyncio
import logging
import subprocess
from functools import wraps

from bidi.algorithm import get_display
from telegram import ForceReply, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

import print_consts

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

async def run_ptouch_info() -> str:
    try:
        output = subprocess.check_output(
            ['ptouch-print', '--info'],
            stderr=subprocess.STDOUT)
        output = output.decode().strip()
        return output
    except subprocess.CalledProcessError as e:
        return e.output.decode()

@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    help_cmd = await run_ptouch_info()
    await update.message.reply_text(help_cmd)

@restricted
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_cmd = await run_ptouch_info()
    await update.message.reply_text(help_cmd)

@restricted
async def print_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the user message."""
    print_text = get_display(update.message.text).splitlines()
    await update.message.reply_text("Printing\n\"" + update.message.text +"\"")
    cmd = ['ptouch-print', '--debug', '--pad', print_consts.PADDING , '--text'] + print_text
    logger.info(cmd)
    subprocess.call(cmd)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(print_consts.TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Add print command handler for all texts (filter out commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, print_sticker))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()    

if __name__ == '__main__':
    main()
