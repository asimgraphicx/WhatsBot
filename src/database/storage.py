"""
Database abstraction layer for multi-tenant Telegram bot.
Currently uses JSON file storage with commented code for MongoDB/PostgreSQL migration.
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from pathlib import Path

# Uncomment for MongoDB support
# from pymongo import MongoClient
# from motor.motor_asyncio import AsyncIOMotorClient

# Uncomment for PostgreSQL support
# import psycopg2
# import asyncpg


class DatabaseManager:
    """
    Database manager that handles storage operations.
    Currently uses JSON files, with commented code for future migration.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.storage_type = config.get('storage', {}).get('type', 'json')
        self.data_dir = config.get('storage', {}).get('data_dir', 'data')
        
        # Ensure data directory exists
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize file paths
        self.users_file = os.path.join(self.data_dir, 'users.json')
        self.bots_file = os.path.join(self.data_dir, 'bots.json')
        self.keywords_file = os.path.join(self.data_dir, 'keywords.json')
        self.settings_file = os.path.join(self.data_dir, 'settings.json')
        
        # Initialize JSON files if they don't exist
        self._initialize_json_files()
        
        # MongoDB initialization (commented out)
        # if config.get('database', {}).get('mongodb', {}).get('enabled'):
        #     self.mongo_client = AsyncIOMotorClient(
        #         config['database']['mongodb']['connection_string']
        #     )
        #     self.mongo_db = self.mongo_client[
        #         config['database']['mongodb']['database_name']
        #     ]
        #     self.users_collection = self.mongo_db['users']
        #     self.bots_collection = self.mongo_db['bots']
        #     self.keywords_collection = self.mongo_db['keywords']
        #     self.settings_collection = self.mongo_db['settings']
        
        # PostgreSQL initialization (commented out)
        # if config.get('database', {}).get('postgresql', {}).get('enabled'):
        #     self.pg_pool = None
        #     asyncio.create_task(self._init_postgresql())
    
    def _initialize_json_files(self):
        """Initialize JSON files with empty structures if they don't exist."""
        default_structures = {
            self.users_file: {},
            self.bots_file: {},
            self.keywords_file: {},
            self.settings_file: {}
        }
        
        for file_path, default_data in default_structures.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    # PostgreSQL async initialization (commented out)
    # async def _init_postgresql(self):
    #     """Initialize PostgreSQL connection pool."""
    #     pg_config = self.config['database']['postgresql']
    #     self.pg_pool = await asyncpg.create_pool(
    #         host=pg_config['host'],
    #         port=pg_config['port'],
    #         database=pg_config['database'],
    #         user=pg_config['user'],
    #         password=pg_config['password']
    #     )
    #     await self._create_pg_tables()
    
    # async def _create_pg_tables(self):
    #     """Create PostgreSQL tables if they don't exist."""
    #     async with self.pg_pool.acquire() as conn:
    #         await conn.execute('''
    #             CREATE TABLE IF NOT EXISTS users (
    #                 user_id BIGINT PRIMARY KEY,
    #                 username VARCHAR(255),
    #                 first_name VARCHAR(255),
    #                 data JSONB,
    #                 created_at TIMESTAMP DEFAULT NOW(),
    #                 updated_at TIMESTAMP DEFAULT NOW()
    #             )
    #         ''')
    #         await conn.execute('''
    #             CREATE TABLE IF NOT EXISTS bots (
    #                 bot_id SERIAL PRIMARY KEY,
    #                 owner_id BIGINT,
    #                 bot_token VARCHAR(255) UNIQUE,
    #                 bot_username VARCHAR(255),
    #                 data JSONB,
    #                 created_at TIMESTAMP DEFAULT NOW(),
    #                 updated_at TIMESTAMP DEFAULT NOW()
    #             )
    #         ''')
    
    def _load_json(self, file_path: str) -> Dict:
        """Load data from JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json(self, file_path: str, data: Dict):
        """Save data to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data by user_id."""
        # JSON implementation
        users = self._load_json(self.users_file)
        return users.get(str(user_id))
        
        # MongoDB implementation (commented out)
        # if self.storage_type == 'mongodb':
        #     return await self.users_collection.find_one({'user_id': user_id})
        
        # PostgreSQL implementation (commented out)
        # if self.storage_type == 'postgresql':
        #     async with self.pg_pool.acquire() as conn:
        #         row = await conn.fetchrow(
        #             'SELECT * FROM users WHERE user_id = $1', user_id
        #         )
        #         return dict(row) if row else None
    
    async def save_user(self, user_id: int, user_data: Dict):
        """Save or update user data."""
        user_data['updated_at'] = datetime.now().isoformat()
        if 'created_at' not in user_data:
            user_data['created_at'] = user_data['updated_at']
        
        # JSON implementation
        users = self._load_json(self.users_file)
        users[str(user_id)] = user_data
        self._save_json(self.users_file, users)
        
        # MongoDB implementation (commented out)
        # if self.storage_type == 'mongodb':
        #     await self.users_collection.update_one(
        #         {'user_id': user_id},
        #         {'$set': user_data},
        #         upsert=True
        #     )
        
        # PostgreSQL implementation (commented out)
        # if self.storage_type == 'postgresql':
        #     async with self.pg_pool.acquire() as conn:
        #         await conn.execute('''
        #             INSERT INTO users (user_id, username, first_name, data, updated_at)
        #             VALUES ($1, $2, $3, $4, NOW())
        #             ON CONFLICT (user_id) DO UPDATE
        #             SET data = $4, updated_at = NOW()
        #         ''', user_id, user_data.get('username'), 
        #              user_data.get('first_name'), json.dumps(user_data))
    
    async def get_bot(self, bot_token: str) -> Optional[Dict]:
        """Get bot data by token."""
        # JSON implementation
        bots = self._load_json(self.bots_file)
        for bot_id, bot_data in bots.items():
            if bot_data.get('bot_token') == bot_token:
                return {**bot_data, 'bot_id': bot_id}
        return None
        
        # MongoDB implementation (commented out)
        # if self.storage_type == 'mongodb':
        #     return await self.bots_collection.find_one({'bot_token': bot_token})
        
        # PostgreSQL implementation (commented out)
        # if self.storage_type == 'postgresql':
        #     async with self.pg_pool.acquire() as conn:
        #         row = await conn.fetchrow(
        #             'SELECT * FROM bots WHERE bot_token = $1', bot_token
        #         )
        #         return dict(row) if row else None
    
    async def save_bot(self, bot_token: str, bot_data: Dict):
        """Save or update bot data."""
        bot_data['updated_at'] = datetime.now().isoformat()
        if 'created_at' not in bot_data:
            bot_data['created_at'] = bot_data['updated_at']
        
        # JSON implementation
        bots = self._load_json(self.bots_file)
        
        # Find existing bot or create new ID
        bot_id = None
        for bid, bdata in bots.items():
            if bdata.get('bot_token') == bot_token:
                bot_id = bid
                break
        
        if not bot_id:
            # Generate new bot ID
            bot_id = str(len(bots) + 1)
        
        bots[bot_id] = {**bot_data, 'bot_token': bot_token}
        self._save_json(self.bots_file, bots)
        
        # MongoDB implementation (commented out)
        # if self.storage_type == 'mongodb':
        #     await self.bots_collection.update_one(
        #         {'bot_token': bot_token},
        #         {'$set': bot_data},
        #         upsert=True
        #     )
    
    async def get_all_bots(self) -> List[Dict]:
        """Get all registered bots."""
        # JSON implementation
        bots = self._load_json(self.bots_file)
        return [
            {**bot_data, 'bot_id': bot_id} 
            for bot_id, bot_data in bots.items()
        ]
        
        # MongoDB implementation (commented out)
        # if self.storage_type == 'mongodb':
        #     cursor = self.bots_collection.find({})
        #     return await cursor.to_list(length=None)
    
    async def get_user_bots(self, owner_id: int) -> List[Dict]:
        """Get all bots owned by a user."""
        # JSON implementation
        bots = self._load_json(self.bots_file)
        return [
            {**bot_data, 'bot_id': bot_id}
            for bot_id, bot_data in bots.items()
            if bot_data.get('owner_id') == owner_id
        ]
        
        # MongoDB implementation (commented out)
        # if self.storage_type == 'mongodb':
        #     cursor = self.bots_collection.find({'owner_id': owner_id})
        #     return await cursor.to_list(length=None)
    
    async def get_settings(self, bot_token: str) -> Dict:
        """Get settings for a specific bot."""
        # JSON implementation
        settings = self._load_json(self.settings_file)
        return settings.get(bot_token, {})
        
        # MongoDB implementation (commented out)
        # if self.storage_type == 'mongodb':
        #     result = await self.settings_collection.find_one({'bot_token': bot_token})
        #     return result.get('settings', {}) if result else {}
    
    async def save_settings(self, bot_token: str, settings_data: Dict):
        """Save settings for a specific bot."""
        # JSON implementation
        settings = self._load_json(self.settings_file)
        settings[bot_token] = settings_data
        self._save_json(self.settings_file, settings)
        
        # MongoDB implementation (commented out)
        # if self.storage_type == 'mongodb':
        #     await self.settings_collection.update_one(
        #         {'bot_token': bot_token},
        #         {'$set': {'settings': settings_data}},
        #         upsert=True
        #     )
    
    async def close(self):
        """Close database connections."""
        # MongoDB close (commented out)
        # if hasattr(self, 'mongo_client'):
        #     self.mongo_client.close()
        
        # PostgreSQL close (commented out)
        # if hasattr(self, 'pg_pool') and self.pg_pool:
        #     await self.pg_pool.close()
        pass
