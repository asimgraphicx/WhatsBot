# Telegram Multi-Tenant Support Bot

A comprehensive multi-tenant Telegram bot system built with Python that allows multiple bot owners to configure and manage their own support bots, with a super admin panel for central management.

## Features

### 🎯 Multi-Tenant Architecture
- Support for multiple bot tokens
- Each bot owner manages their own bot independently
- Isolated settings and configurations per bot
- Super admin panel for managing all bots

### 🤖 Bot Token Activation
- Users provide their bot token from @BotFather
- Automatic token validation
- Instant bot activation and configuration
- Confirmation messages

### 💬 Welcome Message System
- Customizable welcome messages per bot
- Support for dynamic placeholders:
  - `{name}` - User's full name
  - `{firstname}` - User's first name only
  - `{username}` - Username with @ prefix
- Toggle welcome messages on/off
- Live preview of formatted messages

### 📊 Data Storage
- JSON-based storage (default)
- Commented code for MongoDB migration
- Commented code for PostgreSQL migration
- Database configuration placeholders in config.json

### 🛡️ Admin Features
- Super admin panel for bot management
- View all registered bots
- Monitor bot statistics
- User management capabilities

## Installation

### Prerequisites
- Python 3.8 or higher
- A Telegram account
- Bot token from @BotFather

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/asimgraphicx/WhatsBot.git
cd WhatsBot
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your main bot token:
```env
TELEGRAM_BOT_TOKEN=your_main_bot_token_here
```

5. **Configure super admins** (optional)

Edit `config/config.json` and add your Telegram user ID:
```json
{
  "super_admin": {
    "user_ids": [123456789]
  }
}
```

6. **Run the bot**
```bash
cd src
python main.py
```

## Usage

### For Bot Owners

1. **Start the main bot**
   - Message the main bot on Telegram
   - Send `/start` command

2. **Register your bot**
   - Create a new bot with @BotFather
   - Copy the bot token
   - Send the token to the main bot

3. **Configure welcome message**
   - Use `/setwelcome` command
   - Send your custom welcome message
   - Use placeholders: `{name}`, `{firstname}`, `{username}`

4. **Manage settings**
   - `/mybots` - View all your registered bots
   - `/togglewelcome` - Enable/disable welcome messages
   - `/setwelcome` - Update welcome message

### For End Users

1. **Start any registered bot**
   - Find the bot by username
   - Send `/start` command
   - Receive personalized welcome message

### For Super Admins

1. **Access admin panel**
   - Send `/admin` command
   - View all registered bots
   - Monitor system statistics

## Commands Reference

### Main Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start bot and register new bot token |
| `/mybots` | View your registered bots |
| `/setwelcome` | Set custom welcome message |
| `/togglewelcome` | Toggle welcome message on/off |
| `/admin` | Super admin panel (admins only) |
| `/cancel` | Cancel current operation |

### User Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Receive welcome message |

## Project Structure

```
WhatsBot/
├── config/
│   └── config.json          # Configuration file
├── data/                    # JSON data storage
│   ├── users.json          # User data
│   ├── bots.json           # Bot registrations
│   ├── keywords.json       # Keywords (future use)
│   └── settings.json       # Bot settings
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   └── manager.py      # Bot manager
│   ├── database/
│   │   ├── __init__.py
│   │   └── storage.py      # Database layer
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── main_bot_handlers.py    # Main bot handlers
│   │   └── user_bot_handlers.py    # User bot handlers
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py      # Helper functions
│   └── main.py             # Application entry point
├── .env.example            # Environment template
├── .gitignore
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Database Migration

The system currently uses JSON files for storage, but includes commented code for easy migration to MongoDB or PostgreSQL.

### Migrating to MongoDB

1. Uncomment MongoDB dependencies in `requirements.txt`
2. Install dependencies: `pip install pymongo motor`
3. Update `config/config.json`:
```json
{
  "database": {
    "mongodb": {
      "enabled": true,
      "connection_string": "mongodb://localhost:27017/",
      "database_name": "telegram_support_bot"
    }
  }
}
```
4. Uncomment MongoDB code in `src/database/storage.py`

### Migrating to PostgreSQL

1. Uncomment PostgreSQL dependencies in `requirements.txt`
2. Install dependencies: `pip install psycopg2-binary asyncpg`
3. Update `config/config.json`:
```json
{
  "database": {
    "postgresql": {
      "enabled": true,
      "host": "localhost",
      "port": 5432,
      "database": "telegram_support_bot",
      "user": "postgres",
      "password": "your_password"
    }
  }
}
```
4. Uncomment PostgreSQL code in `src/database/storage.py`

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

## Technologies Used

- **Python 3.8+**
- **python-telegram-bot v20+** - Telegram Bot API wrapper
- **python-dotenv** - Environment variable management
- **jsonschema** - JSON validation
- Optional: **pymongo/motor** - MongoDB support
- Optional: **psycopg2/asyncpg** - PostgreSQL support

## Security Considerations

- Never commit `.env` file to version control
- Keep bot tokens secure
- Use environment variables for sensitive data
- Validate all user inputs
- Regularly update dependencies

## Troubleshooting

### Bot not responding
- Check if bot token is correct in `.env`
- Verify bot is running: `python src/main.py`
- Check logs for error messages

### Invalid token error
- Ensure token format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
- Get fresh token from @BotFather
- Verify no extra spaces in token

### Permission denied errors
- Check file permissions in `data/` directory
- Ensure write access to JSON files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue on GitHub or contact the maintainers.

## Roadmap

- [ ] Multi-language support
- [ ] Advanced keyword-based responses
- [ ] Analytics dashboard
- [ ] Broadcast messaging
- [ ] Custom commands per bot
- [ ] File upload support
- [ ] Integration with external APIs
- [ ] Web-based admin panel

## Author

**asimgraphicx**

## Acknowledgments

- python-telegram-bot library contributors
- Telegram Bot API documentation
- Open source community
