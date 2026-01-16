"""
Main bot command handlers.
Handles user registration, bot token activation, and configuration.
"""

from telegram import Update
from telegram.ext import (
    CommandHandler, 
    MessageHandler, 
    filters,
    ContextTypes,
    ConversationHandler
)
import logging
import re

logger = logging.getLogger(__name__)

# Conversation states
WAITING_FOR_TOKEN = 1
WAITING_FOR_WELCOME = 2


class MainBotHandlers:
    """Handlers for the main bot."""
    
    def __init__(self, bot_manager, database, config):
        self.bot_manager = bot_manager
        self.database = database
        self.config = config
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command.
        Prompts user to provide their bot token for activation.
        """
        user = update.effective_user
        
        # Save user info
        await self.database.save_user(user.id, {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
        
        welcome_text = (
            f"👋 Hello {user.first_name}!\n\n"
            f"Welcome to the **Multi-Tenant Support Bot Manager**!\n\n"
            f"To get started:\n"
            f"1️⃣ Create a bot with @BotFather\n"
            f"2️⃣ Send me your bot token\n"
            f"3️⃣ Configure your bot settings\n\n"
            f"📝 **Commands:**\n"
            f"• /start - Start the bot\n"
            f"• /mybots - View your registered bots\n"
            f"• /setwelcome - Set welcome message\n"
            f"• /togglewelcome - Toggle welcome on/off\n\n"
            f"Please send me your bot token to begin:"
        )
        
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown'
        )
        
        # Set conversation state
        context.user_data['awaiting_token'] = True
        return WAITING_FOR_TOKEN
    
    async def receive_token(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle bot token input from user.
        Validates and registers the bot.
        """
        user = update.effective_user
        token = update.message.text.strip()
        
        # Check if user is in token input mode
        if not context.user_data.get('awaiting_token'):
            return
        
        # Validate token format
        if not re.match(r'^\d+:[A-Za-z0-9_-]{35}$', token):
            await update.message.reply_text(
                "❌ Invalid token format!\n\n"
                "Please send a valid bot token from @BotFather.\n"
                "Format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            )
            return WAITING_FOR_TOKEN
        
        # Show processing message
        processing_msg = await update.message.reply_text("🔄 Validating bot token...")
        
        # Register the bot
        success = await self.bot_manager.register_user_bot(token, user.id)
        
        if success:
            # Get bot info
            bot_info = await self.database.get_bot(token)
            
            await processing_msg.edit_text(
                f"✅ **Bot Successfully Activated!**\n\n"
                f"🤖 Bot: @{bot_info.get('bot_username', 'Unknown')}\n"
                f"👤 Owner: {user.first_name}\n\n"
                f"Your bot is now ready! You can configure it using:\n"
                f"• /setwelcome - Customize welcome message\n"
                f"• /togglewelcome - Enable/disable welcome\n"
                f"• /mybots - View all your bots\n\n"
                f"Start your bot now: @{bot_info.get('bot_username', '')}",
                parse_mode='Markdown'
            )
            context.user_data['awaiting_token'] = False
            context.user_data['current_bot_token'] = token
            return ConversationHandler.END
        else:
            await processing_msg.edit_text(
                "❌ **Failed to activate bot!**\n\n"
                "Possible reasons:\n"
                "• Invalid token\n"
                "• Bot doesn't exist\n"
                "• Token already in use\n\n"
                "Please check your token and try again."
            )
            return WAITING_FOR_TOKEN
    
    async def mybots_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Show user's registered bots.
        """
        user = update.effective_user
        user_bots = await self.database.get_user_bots(user.id)
        
        if not user_bots:
            await update.message.reply_text(
                "📭 You don't have any registered bots yet.\n\n"
                "Send me a bot token to get started!"
            )
            return
        
        # Build bots list
        bots_text = "🤖 **Your Registered Bots:**\n\n"
        for i, bot in enumerate(user_bots, 1):
            bot_username = bot.get('bot_username', 'Unknown')
            bot_token = bot.get('bot_token', '')
            status = "🟢 Active" if bot.get('active') else "🔴 Inactive"
            
            bots_text += f"{i}. @{bot_username}\n"
            bots_text += f"   Status: {status}\n"
            bots_text += f"   Token: `{bot_token[:15]}...`\n\n"
        
        bots_text += "\n💡 Use `/setwelcome` to configure your bot's welcome message."
        
        await update.message.reply_text(bots_text, parse_mode='Markdown')
    
    async def setwelcome_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Set custom welcome message for the bot.
        """
        user = update.effective_user
        
        # Get user's bots
        user_bots = await self.database.get_user_bots(user.id)
        
        if not user_bots:
            await update.message.reply_text(
                "❌ You don't have any registered bots.\n"
                "Please send me a bot token first."
            )
            return
        
        # If user has only one bot, use it
        if len(user_bots) == 1:
            context.user_data['current_bot_token'] = user_bots[0].get('bot_token')
        
        # Check if bot token is set
        if 'current_bot_token' not in context.user_data:
            # Show bot selection
            bots_text = "Please select a bot first by clicking on its token:\n\n"
            for bot in user_bots:
                bot_username = bot.get('bot_username', 'Unknown')
                bots_text += f"@{bot_username}\n"
            
            await update.message.reply_text(bots_text)
            return
        
        await update.message.reply_text(
            "📝 **Set Welcome Message**\n\n"
            "Send me the welcome message you want to use.\n\n"
            "**Available placeholders:**\n"
            "• `{name}` - Full name\n"
            "• `{firstname}` - First name only\n"
            "• `{username}` - Username with @\n\n"
            "**Example:**\n"
            "`Hello {name}! Welcome to our support bot.`\n\n"
            "Send your message:",
            parse_mode='Markdown'
        )
        
        context.user_data['awaiting_welcome'] = True
        return WAITING_FOR_WELCOME
    
    async def receive_welcome(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle welcome message input.
        """
        if not context.user_data.get('awaiting_welcome'):
            return
        
        user = update.effective_user
        welcome_message = update.message.text
        
        # Get current bot token
        bot_token = context.user_data.get('current_bot_token')
        
        if not bot_token:
            await update.message.reply_text(
                "❌ No bot selected. Use /mybots to view your bots."
            )
            return
        
        # Get current settings
        settings = await self.database.get_settings(bot_token)
        settings['welcome_message'] = welcome_message
        
        # Save settings
        await self.database.save_settings(bot_token, settings)
        
        # Test the message with user's data
        from ..utils.helpers import format_message
        test_message = format_message(welcome_message, {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        })
        
        await update.message.reply_text(
            f"✅ **Welcome message updated!**\n\n"
            f"**Preview:**\n{test_message}",
            parse_mode='Markdown'
        )
        
        context.user_data['awaiting_welcome'] = False
        return ConversationHandler.END
    
    async def togglewelcome_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Toggle welcome message on/off.
        """
        user = update.effective_user
        
        # Get user's bots
        user_bots = await self.database.get_user_bots(user.id)
        
        if not user_bots:
            await update.message.reply_text(
                "❌ You don't have any registered bots."
            )
            return
        
        # Use the current bot or first bot
        bot_token = context.user_data.get('current_bot_token')
        if not bot_token and user_bots:
            bot_token = user_bots[0].get('bot_token')
            context.user_data['current_bot_token'] = bot_token
        
        if not bot_token:
            await update.message.reply_text("❌ No bot selected.")
            return
        
        # Get and toggle settings
        settings = await self.database.get_settings(bot_token)
        current_status = settings.get('welcome_enabled', True)
        settings['welcome_enabled'] = not current_status
        
        await self.database.save_settings(bot_token, settings)
        
        status_text = "✅ enabled" if settings['welcome_enabled'] else "❌ disabled"
        await update.message.reply_text(
            f"Welcome message is now **{status_text}**!",
            parse_mode='Markdown'
        )
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Super admin panel.
        """
        user = update.effective_user
        
        from ..utils.helpers import is_super_admin
        if not is_super_admin(user.id, self.config):
            await update.message.reply_text("❌ You don't have admin access.")
            return
        
        # Get all bots
        all_bots = await self.database.get_all_bots()
        
        admin_text = "👑 **Super Admin Panel**\n\n"
        admin_text += f"📊 **Statistics:**\n"
        admin_text += f"• Total Bots: {len(all_bots)}\n"
        admin_text += f"• Active Bots: {sum(1 for b in all_bots if b.get('active'))}\n\n"
        
        if all_bots:
            admin_text += "🤖 **Registered Bots:**\n\n"
            for i, bot in enumerate(all_bots[:10], 1):  # Show first 10
                bot_username = bot.get('bot_username', 'Unknown')
                owner_id = bot.get('owner_id')
                admin_text += f"{i}. @{bot_username} (Owner: {owner_id})\n"
        
        await update.message.reply_text(admin_text, parse_mode='Markdown')
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel current operation."""
        context.user_data.clear()
        await update.message.reply_text("❌ Operation cancelled.")
        return ConversationHandler.END


def get_handlers(bot_manager, database, config):
    """
    Get all command handlers for the main bot.
    
    Returns:
        List of handler objects
    """
    handlers = MainBotHandlers(bot_manager, database, config)
    
    # Conversation handler for bot token input
    token_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start_command)],
        states={
            WAITING_FOR_TOKEN: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handlers.receive_token
                )
            ],
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel_command)],
        per_message=False
    )
    
    # Conversation handler for welcome message
    welcome_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('setwelcome', handlers.setwelcome_command)],
        states={
            WAITING_FOR_WELCOME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handlers.receive_welcome
                )
            ],
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel_command)],
        per_message=False
    )
    
    return [
        token_conv_handler,
        welcome_conv_handler,
        CommandHandler('mybots', handlers.mybots_command),
        CommandHandler('togglewelcome', handlers.togglewelcome_command),
        CommandHandler('admin', handlers.admin_command),
    ]


# Helper functions for bot manager
def get_start_handler():
    """Placeholder - handlers are created with full context."""
    pass

def get_setwelcome_handler():
    """Placeholder - handlers are created with full context."""
    pass

def get_togglewelcome_handler():
    """Placeholder - handlers are created with full context."""
    pass

def get_mybot_handler():
    """Placeholder - handlers are created with full context."""
    pass

def get_admin_handler():
    """Placeholder - handlers are created with full context."""
    pass

def get_token_handler():
    """Placeholder - handlers are created with full context."""
    pass
