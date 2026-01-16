"""
Main entry point for the Telegram Multi-Tenant Support Bot.
"""

import os
import json
import logging
import asyncio
from pathlib import Path
from telegram.ext import Application, ApplicationBuilder
from dotenv import load_dotenv

from database import DatabaseManager
from bot import BotManager
from handlers import main_bot_handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from config.json."""
    config_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'config',
        'config.json'
    )
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found at {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        raise


async def main():
    """Main function to run the bot."""
    # Load environment variables
    load_dotenv()
    
    # Get main bot token from environment
    main_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not main_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        logger.info("Please create a .env file with your bot token:")
        logger.info("TELEGRAM_BOT_TOKEN=your_token_here")
        return
    
    # Load configuration
    config = load_config()
    
    # Update data directory path to absolute
    config['storage']['data_dir'] = os.path.join(
        os.path.dirname(__file__),
        '..',
        config['storage']['data_dir']
    )
    
    logger.info("Starting Telegram Multi-Tenant Support Bot...")
    logger.info(f"Storage type: {config['storage']['type']}")
    
    # Initialize database
    database = DatabaseManager(config)
    
    # Initialize bot manager
    bot_manager = BotManager(database)
    
    # Build main bot application
    app = ApplicationBuilder().token(main_bot_token).build()
    
    # Get and add handlers
    handlers = main_bot_handlers.get_handlers(bot_manager, database, config)
    for handler in handlers:
        app.add_handler(handler)
    
    logger.info("Main bot initialized successfully")
    logger.info(f"Bot is running. Press Ctrl+C to stop.")
    
    try:
        # Start the bot
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        
        # Keep the bot running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
    finally:
        # Cleanup
        await app.stop()
        await app.shutdown()
        await bot_manager.shutdown()
        logger.info("Bot stopped successfully")


if __name__ == '__main__':
    asyncio.run(main())
