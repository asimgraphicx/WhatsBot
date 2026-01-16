# Usage Examples

This document provides practical examples of using the Telegram Multi-Tenant Support Bot.

## Example 1: Basic Setup

### Creating Your First Support Bot

1. **Start the main bot:**
```
You: /start
Bot: 👋 Hello John!
     Welcome to the Multi-Tenant Support Bot Manager!
     
     To get started:
     1️⃣ Create a bot with @BotFather
     2️⃣ Send me your bot token
     3️⃣ Configure your bot settings
     
     Please send me your bot token to begin:
```

2. **Send bot token:**
```
You: 987654321:ABCdefGHIjklMNOpqrsTUVwxyz
Bot: 🔄 Validating bot token...
     ✅ Bot Successfully Activated!
     
     🤖 Bot: @my_support_bot
     👤 Owner: John
     
     Your bot is now ready! You can configure it using:
     • /setwelcome - Customize welcome message
     • /togglewelcome - Enable/disable welcome
     • /mybots - View all your bots
     
     Start your bot now: @my_support_bot
```

## Example 2: Setting Welcome Messages

### Simple Welcome Message

```
You: /setwelcome
Bot: 📝 Set Welcome Message
     
     Send me the welcome message you want to use.
     
     Available placeholders:
     • {name} - Full name
     • {firstname} - First name only
     • {username} - Username with @
     
     Send your message:

You: Hello {firstname}! Welcome to our support team.
Bot: ✅ Welcome message updated!
     
     Preview:
     Hello John! Welcome to our support team.
```

### Advanced Welcome Message

```
You: /setwelcome
Bot: [waiting for message...]

You: 👋 Hi {name}!

Welcome to **TechSupport Bot** 🤖

We're here to help you 24/7 with:
• Technical issues
• Product questions
• Account support

Type your question and our team will respond shortly!

Bot: ✅ Welcome message updated!
     
     Preview:
     👋 Hi John Doe!
     
     Welcome to **TechSupport Bot** 🤖
     
     We're here to help you 24/7 with:
     • Technical issues
     • Product questions
     • Account support
     
     Type your question and our team will respond shortly!
```

## Example 3: Managing Multiple Bots

### View All Your Bots

```
You: /mybots
Bot: 🤖 Your Registered Bots:
     
     1. @support_bot_main
        Status: 🟢 Active
        Token: 123456789:ABCD...
     
     2. @help_bot_secondary
        Status: 🟢 Active
        Token: 987654321:WXYZ...
     
     3. @feedback_collector
        Status: 🟢 Active
        Token: 555666777:MNOP...
     
     💡 Use /setwelcome to configure your bot's welcome message.
```

## Example 4: Toggle Welcome Messages

### Disabling Welcome

```
You: /togglewelcome
Bot: Welcome message is now ❌ disabled!
```

### Enabling Welcome

```
You: /togglewelcome
Bot: Welcome message is now ✅ enabled!
```

## Example 5: Super Admin Panel

### Viewing All Bots (Admin Only)

```
You: /admin
Bot: 👑 Super Admin Panel
     
     📊 Statistics:
     • Total Bots: 15
     • Active Bots: 12
     
     🤖 Registered Bots:
     
     1. @support_bot_main (Owner: 123456789)
     2. @help_bot_secondary (Owner: 123456789)
     3. @customer_service_bot (Owner: 987654321)
     4. @tech_support_bot (Owner: 987654321)
     5. @feedback_bot (Owner: 555666777)
     ...
```

## Example 6: End-User Experience

### User Starts Support Bot

```
User: /start
Support Bot: 👋 Hi Sarah Johnson!
             
             Welcome to **TechSupport Bot** 🤖
             
             We're here to help you 24/7 with:
             • Technical issues
             • Product questions
             • Account support
             
             Type your question and our team will respond shortly!
```

### Different Users Get Personalized Messages

```
User A (John Doe, @johndoe):
"Hello John Doe! Your username is @johndoe."

User B (Jane Smith, no username):
"Hello Jane Smith! Welcome to our support."

User C (Mike, @mike123):
"Hello Mike! Your username is @mike123."
```

## Example 7: Multi-Brand Setup

### Company with Multiple Brands

```
Main Bot Owner: registers 3 bots
1. @brand_a_support - for Brand A customers
2. @brand_b_help - for Brand B customers  
3. @brand_c_service - for Brand C customers

Each bot has custom welcome:

Brand A: "Welcome to Brand A Premium Support! 💎"
Brand B: "Hi {firstname}! Brand B is here to help! 🚀"
Brand C: "Hello {name}! Thanks for choosing Brand C! ⭐"
```

## Example 8: Error Handling

### Invalid Token

```
You: invalid_token_format
Bot: ❌ Invalid token format!
     
     Please send a valid bot token from @BotFather.
     Format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Token Doesn't Exist

```
You: 999999999:ABCdefGHIjklMNOpqrsTUVwxyz
Bot: 🔄 Validating bot token...
     ❌ Failed to activate bot!
     
     Possible reasons:
     • Invalid token
     • Bot doesn't exist
     • Token already in use
     
     Please check your token and try again.
```

## Example 9: Placeholder Demonstration

### Message Template

```
"Hello {name}! Your username is {username}. Welcome {firstname}!"
```

### Results for Different Users

**User 1:** John Doe (@johndoe)
```
"Hello John Doe! Your username is @johndoe. Welcome John!"
```

**User 2:** Jane Smith (no username)
```
"Hello Jane Smith! Your username is Jane Smith. Welcome Jane!"
```

**User 3:** Mike (no last name, @mike99)
```
"Hello Mike! Your username is @mike99. Welcome Mike!"
```

## Example 10: Workflow Integration

### Customer Support Team

```
1. Support Manager creates bot with @BotFather
2. Configures welcome message in main bot
3. Shares @support_bot with team
4. Team members start receiving support requests
5. Manager monitors via /admin panel
```

### SaaS Product

```
1. Product creates support bot
2. Sets welcome: "Hi {name}! Need help with ProductX?"
3. Adds bot link to website
4. Users click link -> start bot -> get instant greeting
5. Support team handles requests in Telegram
```

## Example 11: Advanced Configuration

### Multi-Language Welcome (Manual)

```
Setup different bots for different languages:

@support_en: "Hello {name}! How can we help?"
@support_es: "¡Hola {name}! ¿Cómo podemos ayudarte?"
@support_fr: "Bonjour {name}! Comment pouvons-nous vous aider?"
@support_de: "Hallo {name}! Wie können wir helfen?"
```

## Example 12: Testing Your Bot

### Quick Test Checklist

```
✅ 1. Register bot token
    You: [send token]
    Expected: Success confirmation

✅ 2. Set welcome message
    You: /setwelcome
    You: Hello {firstname}!
    Expected: Preview with your name

✅ 3. Toggle welcome
    You: /togglewelcome
    Expected: Status change confirmation

✅ 4. View bots
    You: /mybots
    Expected: List of your bots

✅ 5. Test support bot
    Open support bot
    You: /start
    Expected: Welcome message with your name
```

## Tips and Best Practices

### Welcome Message Tips

1. **Keep it concise** - Users prefer short, clear messages
2. **Use emojis** - Makes messages more friendly 👋 🤖 ✨
3. **Include next steps** - Tell users what to do next
4. **Personalize** - Use {firstname} for warmth
5. **Brand it** - Include your brand name

### Examples of Good Welcome Messages

```
✅ "Hi {firstname}! Welcome to TechCorp Support. How can we help?"

✅ "👋 Hello {name}! 
    Thanks for contacting us. What's on your mind?"

✅ "Welcome {firstname}! 🎉
    Our support team is ready to help you!"
```

### Examples of Poor Welcome Messages

```
❌ "Hello." (too short, no personality)

❌ "Welcome to our support system. Please note that we are 
    available Monday through Friday from 9 AM to 5 PM EST 
    excluding holidays. Please provide your account number,
    full name, email address, and a detailed description..."
    (way too long)

❌ "User {user_id} has initiated contact." 
    (impersonal, robotic)
```

## Troubleshooting Examples

### Issue: Bot Not Responding

```
Problem: Registered bot but it doesn't respond
Solution: 
1. Check if bot is active: /mybots
2. Verify token is correct
3. Try toggling welcome: /togglewelcome
4. Re-register if needed
```

### Issue: Wrong Name in Welcome

```
Problem: Welcome shows wrong name
Solution:
1. User needs to set Telegram first name
2. If no first name, system uses "User"
3. Update Telegram profile settings
```

---

For more examples and support, check the README.md and ARCHITECTURE.md files.
