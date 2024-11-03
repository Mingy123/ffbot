import discord
import asyncio
from datetime import datetime
import pytz
from discord.ext import tasks, commands
from ffio import getRate

TOKEN = os.environ['FF_DISCORD_TOKEN']
USER_ID = '549150218424287232'  # Replace with your Discord user ID

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
last_message = None
timezone = pytz.timezone("Singapore")

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    check_rate.start()

@tasks.loop(minutes=1)
async def check_rate():
    rate_from, rate_to = await getRate()
    rate_to = 1/rate_to
    if rate_from > 2.3:
        await send_message_from(rate_from)
    else:
        await send_message_to(rate_to)
    #await user.send(message)

async def send_message_from(rate):
    global last_message
    user = await bot.fetch_user(USER_ID)
    lm = last_message
    content = f"XMR -> LTC at {rate} ({time_as_str()})"
    if lm is None or rate > 2.35:
        last_message = await user.send(content)
        return

    last_time = lm.edited_at if lm.edited_at is not None else lm.created_at
    diff = datetime.now(timezone) - last_time

    # over 30 minutes since the last send/edit
    if diff.seconds // 60 >= 30:
        last_message = await user.send(content)
    else:
        await last_message.edit(content=content)

async def send_message_to(rate):
    global last_message
    user = await bot.fetch_user(USER_ID)
    lm = last_message
    content = f"LTC -> XMR at {rate} ({time_as_str()})"
    if lm is None or rate < 2.15:
        last_message = await user.send(content)
        return

    last_time = lm.edited_at if lm.edited_at is not None else lm.created_at
    diff = datetime.now(timezone) - last_time

    # over 30 minutes since the last send/edit
    if diff.seconds // 60 >= 30:
        last_message = await user.send(content)
    else:
        await last_message.edit(content=content)

def time_as_str():
    return datetime.now(timezone).strftime("%H:%M %p")

@check_rate.before_loop
async def before_check_rate():
    await bot.wait_until_ready()

bot.run(TOKEN)
