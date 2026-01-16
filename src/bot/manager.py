"""
Multi-tenant bot manager.
Handles multiple bot instances and their lifecycle.
"""

from typing import Dict, Optional
from telegram import Update
from telegram.ext import Application, ApplicationBuilder
import logging

logger = logging.getLogger(__name__)


class BotManager:
    """
    Manages multiple bot instances for multi-tenant support.
    Each bot owner can have their own bot token(s).
    """
    
    def __init__(self, database):
        self.database = database
        self.active_bots: Dict[str, Application] = {}
        self.main_bot_token: Optional[str] = None
        self.main_bot: Optional[Application] = None
    
    async def initialize_main_bot(self, token: str, handlers_module) -> Application:
        """
        Initialize the main bot that handles bot registration and super admin functions.
        
        Args:
            token: Main bot token
            handlers_module: Module containing command handlers
            
        Returns:
            The main bot Application instance
        """
        self.main_bot_token = token
        
        # Build the application
        app = ApplicationBuilder().token(token).build()
        
        # Add handlers
        app.add_handler(handlers_module.get_start_handler())
        app.add_handler(handlers_module.get_setwelcome_handler())
        app.add_handler(handlers_module.get_togglewelcome_handler())
        app.add_handler(handlers_module.get_mybot_handler())
        app.add_handler(handlers_module.get_admin_handler())
        
        # Add message handler for bot token input
        app.add_handler(handlers_module.get_token_handler())
        
        self.main_bot = app
        return app
    
    async def register_user_bot(self, bot_token: str, owner_id: int) -> bool:
        """
        Register a user's bot token.
        
        Args:
            bot_token: The bot token to register
            owner_id: Telegram user ID of the bot owner
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Check if bot already exists
            existing_bot = await self.database.get_bot(bot_token)
            if existing_bot:
                logger.info(f"Bot token already registered for user {owner_id}")
                return True
            
            # Validate the token by trying to connect
            from ..utils.helpers import validate_bot_token
            bot_info = await validate_bot_token(bot_token)
            
            if not bot_info:
                logger.warning(f"Invalid bot token provided by user {owner_id}")
                return False
            
            # Save bot information
            bot_data = {
                'bot_token': bot_token,
                'owner_id': owner_id,
                'bot_username': bot_info.get('username'),
                'bot_id': bot_info.get('id'),
                'active': True
            }
            await self.database.save_bot(bot_token, bot_data)
            
            # Initialize default settings
            default_settings = {
                'welcome_message': 'Hello {name}! Welcome to our support bot.',
                'welcome_enabled': True
            }
            await self.database.save_settings(bot_token, default_settings)
            
            logger.info(f"Successfully registered bot @{bot_info.get('username')} for user {owner_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error registering bot: {e}")
            return False
    
    async def start_user_bot(self, bot_token: str):
        """
        Start a user's bot instance.
        
        Args:
            bot_token: The bot token to start
        """
        if bot_token in self.active_bots:
            logger.info(f"Bot {bot_token[:10]}... already running")
            return
        
        try:
            # Build the application for user bot
            app = ApplicationBuilder().token(bot_token).build()
            
            # Add basic handlers for user-facing bot
            from ..handlers import user_bot_handlers
            app.add_handler(user_bot_handlers.get_user_start_handler(self.database, bot_token))
            
            # Start the bot
            await app.initialize()
            await app.start()
            
            self.active_bots[bot_token] = app
            logger.info(f"Started user bot {bot_token[:10]}...")
            
        except Exception as e:
            logger.error(f"Error starting user bot: {e}")
    
    async def stop_user_bot(self, bot_token: str):
        """
        Stop a user's bot instance.
        
        Args:
            bot_token: The bot token to stop
        """
        if bot_token not in self.active_bots:
            return
        
        try:
            app = self.active_bots[bot_token]
            await app.stop()
            await app.shutdown()
            del self.active_bots[bot_token]
            logger.info(f"Stopped user bot {bot_token[:10]}...")
        except Exception as e:
            logger.error(f"Error stopping user bot: {e}")
    
    async def get_bot_settings(self, bot_token: str) -> Dict:
        """Get settings for a specific bot."""
        return await self.database.get_settings(bot_token)
    
    async def update_bot_settings(self, bot_token: str, settings: Dict):
        """Update settings for a specific bot."""
        await self.database.save_settings(bot_token, settings)
    
    async def shutdown(self):
        """Shutdown all bot instances."""
        # Stop all user bots
        for bot_token in list(self.active_bots.keys()):
            await self.stop_user_bot(bot_token)
        
        # Stop main bot
        if self.main_bot:
            await self.main_bot.stop()
            await self.main_bot.shutdown()
        
        # Close database
        await self.database.close()
        logger.info("All bots shut down successfully")
