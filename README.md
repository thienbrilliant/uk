# Discord Controlled Repeater Bot + Philosophy Corpus
Files:
- bot.py : Safe controlled repeater bot (Python, discord.py)
- .env.example : example environment file
- utils.py : small helpers
- philosophies.txt : 100,000+ original philosophical sentences (one per line)

Usage:
1. Copy .env.example to .env and fill DISCORD_TOKEN and OWNER_ID.
2. Install dependencies:
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -U discord.py python-dotenv
3. Run:
   python bot.py

philosophies.txt is generated for learning/creative use. Don't use it for spam.
