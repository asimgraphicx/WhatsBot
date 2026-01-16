"""
Utility functions for bot operations.
"""

import re
from typing import Optional, Dict
from telegram import Bot
from telegram.error import TelegramError


async def validate_bot_token(token: str) -> Optional[Dict]:
    """
    Validate a Telegram bot token by attempting to connect.
    
    Args:
        token: The bot token to validate
        
    Returns:
        Dict with bot info if valid, None otherwise
    """
    if not token or not re.match(r'^\d+:[A-Za-z0-9_-]{35}$', token):
        return None
    
    try:
        bot = Bot(token=token)
        bot_info = await bot.get_me()
        return {
            'id': bot_info.id,
            'username': bot_info.username,
            'first_name': bot_info.first_name,
            'is_bot': bot_info.is_bot
        }
    except TelegramError:
        return None


def format_message(template: str, user_data: Dict) -> str:
    """
    Format a message template with user data placeholders.
    
    Supported placeholders:
    - {name}: Full name (first_name + last_name)
    - {username}: Username with @ prefix
    - {firstname}: First name only
    
    Args:
        template: Message template with placeholders
        user_data: Dictionary containing user information
        
    Returns:
        Formatted message string
    """
    first_name = user_data.get('first_name', '')
    last_name = user_data.get('last_name', '')
    username = user_data.get('username', '')
    
    # Build full name
    name_parts = [first_name, last_name]
    full_name = ' '.join(filter(None, name_parts)) or 'User'
    
    # Format username with @ if present
    formatted_username = f"@{username}" if username else full_name
    
    # Replace placeholders
    message = template
    message = message.replace('{name}', full_name)
    message = message.replace('{username}', formatted_username)
    message = message.replace('{firstname}', first_name or 'User')
    
    return message


def is_super_admin(user_id: int, config: Dict) -> bool:
    """
    Check if a user is a super admin.
    
    Args:
        user_id: Telegram user ID
        config: Configuration dictionary
        
    Returns:
        True if user is super admin, False otherwise
    """
    super_admin_ids = config.get('super_admin', {}).get('user_ids', [])
    return user_id in super_admin_ids
