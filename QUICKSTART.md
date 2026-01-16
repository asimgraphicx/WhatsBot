# Quick Start Guide

This guide will help you get your Telegram Multi-Tenant Support Bot up and running in 5 minutes.

## Prerequisites

- Python 3.8 or higher installed
- A Telegram account
- 5 minutes of your time

## Step 1: Create Your Main Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` to create a new bot
3. Follow the prompts:
   - Choose a name (e.g., "My Support Bot Manager")
   - Choose a username (e.g., "my_support_manager_bot")
4. Copy the bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Configure the Bot

1. Navigate to the project directory:
```bash
cd WhatsBot
```

2. Copy the environment template:
```bash
cp .env.example .env
```

3. Edit `.env` and paste your bot token:
```env
TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
```

4. (Optional) Get your Telegram user ID:
   - Message `@userinfobot` on Telegram
   - Copy your ID (e.g., `123456789`)

5. (Optional) Add yourself as super admin:
   - Edit `config/config.json`
   - Add your user ID to `super_admin.user_ids` array:
   ```json
   {
     "super_admin": {
       "user_ids": [123456789]
     }
   }
   ```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Start the Bot

```bash
cd src
python main.py
```

You should see:
```
INFO - Starting Telegram Multi-Tenant Support Bot...
INFO - Storage type: json
INFO - Main bot initialized successfully
INFO - Bot is running. Press Ctrl+C to stop.
```

## Step 5: Test the Bot

### Register Your First Support Bot

1. Create another bot with @BotFather (this will be your actual support bot)
2. Copy its token
3. Open your main bot in Telegram
4. Send `/start`
5. Paste the token of your support bot
6. Wait for confirmation ✅

### Configure Welcome Message

1. In the main bot, send `/setwelcome`
2. Type your custom message:
   ```
   Hello {name}! 👋
   
   Welcome to our support system. How can we help you today?
   ```
3. Receive confirmation with preview

### Test Your Support Bot

1. Open your support bot (the second one you created)
2. Send `/start`
3. You should receive your custom welcome message!

## Commands Cheat Sheet

### Main Bot (Manager)
- `/start` - Register a new bot
- `/mybots` - List your bots
- `/setwelcome` - Set welcome message
- `/togglewelcome` - Enable/disable welcome
- `/admin` - Admin panel (if you're a super admin)

### Support Bots (User-facing)
- `/start` - Get welcome message

## What's Next?

- Customize your welcome messages with placeholders
- Register multiple support bots
- Share your support bot with users
- Monitor via admin panel

## Troubleshooting

**Bot not responding?**
- Check your token in `.env`
- Make sure the bot is running
- Check terminal for errors

**Can't register bot?**
- Verify token format is correct
- Make sure bot token is valid
- Try getting a new token from @BotFather

**Need help?**
- Check the full README.md
- Open an issue on GitHub

## Example Use Cases

### Customer Support
Register a support bot for your business, customize the welcome message, and share the bot with customers.

### Community Management
Create multiple support bots for different communities, each with custom welcome messages.

### Multi-Brand Support
Manage support bots for multiple brands from one central system.

---

🎉 Congratulations! You now have a fully functional multi-tenant Telegram support bot system!
