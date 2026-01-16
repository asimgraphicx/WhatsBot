# Architecture Documentation

## System Overview

The Telegram Multi-Tenant Support Bot is a Python-based system that allows multiple bot owners to manage their own support bots through a single main bot interface. The system uses a modular architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Main Bot                              │
│  (Bot Token Registration & Configuration Interface)         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ manages
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Bot Manager                               │
│  - Token validation                                          │
│  - Bot lifecycle management                                  │
│  - Settings management                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ uses
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Database Manager                              │
│  - JSON file storage (default)                               │
│  - MongoDB support (commented)                               │
│  - PostgreSQL support (commented)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ stores
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   Data Files                                 │
│  - users.json: User information                              │
│  - bots.json: Registered bot tokens                          │
│  - settings.json: Bot-specific settings                      │
│  - keywords.json: Keywords (future use)                      │
└──────────────────────────────────────────────────────────────┘
```

## Component Structure

### 1. Main Application (`src/main.py`)

**Responsibilities:**
- Application initialization
- Configuration loading
- Bot lifecycle management
- Handler registration

**Key Functions:**
- `load_config()`: Loads configuration from JSON
- `main()`: Entry point, initializes and runs the bot

### 2. Database Layer (`src/database/`)

#### `storage.py`

**Responsibilities:**
- Data persistence abstraction
- CRUD operations for users, bots, and settings
- Database migration support

**Key Classes:**
- `DatabaseManager`: Main database interface

**Methods:**
- `get_user(user_id)`: Retrieve user data
- `save_user(user_id, data)`: Save user data
- `get_bot(token)`: Get bot by token
- `save_bot(token, data)`: Save bot data
- `get_settings(token)`: Get bot settings
- `save_settings(token, data)`: Save bot settings
- `get_user_bots(owner_id)`: Get all bots for a user
- `get_all_bots()`: Get all registered bots

**Migration Support:**
- Commented MongoDB code for NoSQL migration
- Commented PostgreSQL code for SQL migration

### 3. Bot Management (`src/bot/`)

#### `manager.py`

**Responsibilities:**
- Multi-tenant bot management
- Bot registration and validation
- Bot lifecycle (start/stop)
- Settings management

**Key Classes:**
- `BotManager`: Manages multiple bot instances

**Methods:**
- `initialize_main_bot()`: Set up the main bot
- `register_user_bot()`: Register a new bot token
- `start_user_bot()`: Start a user's bot
- `stop_user_bot()`: Stop a user's bot
- `get_bot_settings()`: Get bot configuration
- `update_bot_settings()`: Update bot configuration

### 4. Handlers (`src/handlers/`)

#### `main_bot_handlers.py`

**Responsibilities:**
- Handle commands on the main bot
- User interaction flows
- Conversation management

**Key Classes:**
- `MainBotHandlers`: Handler collection

**Commands:**
- `/start`: Bot registration flow
- `/mybots`: List user's bots
- `/setwelcome`: Set welcome message
- `/togglewelcome`: Toggle welcome on/off
- `/admin`: Super admin panel
- `/cancel`: Cancel operation

**Conversation States:**
- `WAITING_FOR_TOKEN`: Awaiting bot token input
- `WAITING_FOR_WELCOME`: Awaiting welcome message

#### `user_bot_handlers.py`

**Responsibilities:**
- Handle commands on user-facing bots
- Welcome message delivery

**Functions:**
- `user_bot_start()`: Handle /start on user bots
- `get_user_start_handler()`: Create handler for specific bot

### 5. Utilities (`src/utils/`)

#### `helpers.py`

**Responsibilities:**
- Common utility functions
- Token validation
- Message formatting

**Functions:**
- `validate_bot_token(token)`: Validate Telegram bot token
- `format_message(template, user_data)`: Format messages with placeholders
- `is_super_admin(user_id, config)`: Check admin status

## Data Flow

### Bot Registration Flow

```
User -> /start -> Main Bot
         ↓
Main Bot -> Request Token
         ↓
User -> Sends Token
         ↓
Main Bot -> Validate Token (API Call)
         ↓
Bot Manager -> Save to Database
         ↓
Main Bot -> Confirmation Message -> User
```

### Welcome Message Configuration Flow

```
User -> /setwelcome -> Main Bot
         ↓
Main Bot -> Request Message
         ↓
User -> Sends Message
         ↓
Bot Manager -> Save to Settings
         ↓
Main Bot -> Preview -> User
```

### User Interaction Flow (Support Bot)

```
End User -> /start -> Support Bot
           ↓
Support Bot -> Get Settings from Database
           ↓
Support Bot -> Format Welcome Message
           ↓
Support Bot -> Send to End User
```

## Database Schema

### users.json
```json
{
  "123456789": {
    "user_id": 123456789,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

### bots.json
```json
{
  "1": {
    "bot_token": "123456789:ABCdefGHI...",
    "owner_id": 123456789,
    "bot_username": "my_support_bot",
    "bot_id": 987654321,
    "active": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

### settings.json
```json
{
  "123456789:ABCdefGHI...": {
    "welcome_message": "Hello {name}! Welcome to our support.",
    "welcome_enabled": true
  }
}
```

## Configuration

### config.json Structure

```json
{
  "storage": {
    "type": "json",
    "data_dir": "data"
  },
  "database": {
    "mongodb": {
      "enabled": false,
      "connection_string": "mongodb://localhost:27017/",
      "database_name": "telegram_support_bot"
    },
    "postgresql": {
      "enabled": false,
      "host": "localhost",
      "port": 5432,
      "database": "telegram_support_bot",
      "user": "postgres",
      "password": ""
    }
  },
  "super_admin": {
    "user_ids": []
  },
  "bot": {
    "default_language": "en",
    "max_bots_per_user": 5
  }
}
```

## Security Considerations

### Token Security
- Bot tokens stored in database
- Environment variables for main bot token
- No tokens in source code

### Access Control
- Super admin user ID whitelist
- Bot ownership validation
- User-specific bot access

### Data Protection
- User data isolated by ID
- Bot settings isolated by token
- No cross-tenant data access

## Extensibility

### Adding New Commands

1. Create handler in `main_bot_handlers.py`:
```python
async def my_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handler logic
    pass
```

2. Add to handler list in `get_handlers()`:
```python
CommandHandler('mycommand', handlers.my_command)
```

### Adding Database Fields

1. Update save operation in `storage.py`:
```python
user_data['new_field'] = value
```

2. Access in handlers:
```python
user = await self.database.get_user(user_id)
new_value = user.get('new_field')
```

### Migrating to MongoDB

1. Uncomment MongoDB imports in `storage.py`
2. Uncomment MongoDB initialization code
3. Uncomment MongoDB methods
4. Update `config.json` to enable MongoDB
5. Install pymongo: `pip install pymongo motor`

### Migrating to PostgreSQL

1. Uncomment PostgreSQL imports in `storage.py`
2. Uncomment PostgreSQL initialization code
3. Uncomment PostgreSQL methods
4. Update `config.json` to enable PostgreSQL
5. Install psycopg2: `pip install psycopg2-binary asyncpg`

## Performance Considerations

### Scalability
- JSON storage suitable for < 1000 bots
- MongoDB recommended for 1000+ bots
- PostgreSQL recommended for complex queries

### Optimization
- Use database indexing (MongoDB/PostgreSQL)
- Implement caching for frequently accessed settings
- Use connection pooling for database connections

## Future Enhancements

- [ ] Webhook support instead of polling
- [ ] Message templates system
- [ ] Analytics and metrics
- [ ] Broadcast messaging
- [ ] Custom commands per bot
- [ ] Rate limiting
- [ ] Logging system
- [ ] Backup/restore functionality
- [ ] API for external integrations
