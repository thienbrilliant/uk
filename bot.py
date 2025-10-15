import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID") or 0)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# SAFETY CONFIG
MAX_REPEATS = 5
MIN_DELAY = 1.0
USER_COOLDOWN = 10

user_last_used = {}

def is_owner(ctx):
    return ctx.author.id == OWNER_ID

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")

@bot.command(name="repeat")
@commands.check(lambda ctx: is_owner(ctx))
async def repeat(ctx, times: int, delay: float, *, message: str):
    now = asyncio.get_event_loop().time()
    last = user_last_used.get(ctx.author.id, 0)
    if now - last < USER_COOLDOWN:
        await ctx.reply(f"Bạn vừa dùng lệnh, chờ {int(USER_COOLDOWN - (now-last))}s nữa.", mention_author=False)
        return
    user_last_used[ctx.author.id] = now

    if times < 1 or times > MAX_REPEATS:
        await ctx.reply(f"Sai: times phải từ 1 tới {MAX_REPEATS}.", mention_author=False)
        return
    if delay < MIN_DELAY:
        await ctx.reply(f"Sai: delay tối thiểu là {MIN_DELAY} giây để tránh spam.", mention_author=False)
        return

    await ctx.reply(f"Bắt đầu gửi {times} lần với delay {delay}s (chỉ trên server này).", mention_author=False)

    for i in range(times):
        try:
            await ctx.channel.send(f"{message}")
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            await ctx.channel.send(f"Lỗi khi gửi (bị rate limit hoặc quyền): {e}")
            break

@repeat.error
async def repeat_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Chỉ owner mới được sử dụng lệnh này.", mention_author=False)
    else:
        await ctx.reply(f"Lỗi: {error}", mention_author=False)

@bot.command(name="announce")
@commands.check(lambda ctx: is_owner(ctx))
async def announce(ctx, *, message: str):
    await ctx.send(f"📢 Announcement: {message}")

if __name__ == '__main__':
    if not TOKEN:
        print("Missing DISCORD_TOKEN. Put your token into a .env file.")
    else:
        bot.run(TOKEN)
