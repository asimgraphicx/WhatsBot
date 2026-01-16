"""
User-facing bot handlers.
These handlers are added to each user's bot instance.
"""

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import logging

logger = logging.getLogger(__name__)


async def user_bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE, database, bot_token):
    """
    Handle /start command on user-facing bots.
    Sends welcome message if enabled.
    """
    user = update.effective_user
    
    # Save user interaction
    await database.save_user(user.id, {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    })
    
    # Get bot settings
    settings = await database.get_settings(bot_token)
    
    # Check if welcome is enabled
    if not settings.get('welcome_enabled', True):
        await update.message.reply_text(
            "Hello! How can I help you today?"
        )
        return
    
    # Get welcome message
    welcome_template = settings.get(
        'welcome_message',
        'Hello {name}! Welcome to our support bot.'
    )
    
    # Format message with user data
    from ..utils.helpers import format_message
    welcome_message = format_message(welcome_template, {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username
    })
    
    await update.message.reply_text(welcome_message)


def get_user_start_handler(database, bot_token):
    """
    Create a start handler for a specific user bot.
    
    Args:
        database: Database manager instance
        bot_token: Bot token for this instance
        
    Returns:
        CommandHandler for /start
    """
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await user_bot_start(update, context, database, bot_token)
    
    return CommandHandler('start', handler)
