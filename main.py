import discord 
from discord.ext import commands , tasks
import os 
import logging
from dotenv import load_dotenv 
import time

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.messages = True 
intents.presences = True 

bot = commands.Bot(command_prefix='!', intents=intents)

periodic_task_running = False 
time_passed = -5

@bot.event 
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # but doesnt start task here waits for u to come online

@tasks.loop(minutes=5)
async def periodic_message():
    global time_passed
    user = bot.get_user(723428018692816938)
    if user:
        time_passed += 5
        await user.send(f"{time_passed} minutes have passed!")

@bot.event 
async def on_presence_update(before, after):
    global periodic_task_running 
    if after.id == 723428018692816938:
        if before.status == discord.Status.offline and after.status != discord.Status.offline:
            if not periodic_task_running:
                print("You came online! Starting periodic messages...")
                periodic_task_running = True 
                periodic_message.start()
        elif before.status != discord.Status.offline and after.status == discord.Status.offline: 
            if periodic_task_running: 
                print("You went offline! Stopping periodic messages.")
                periodic_task_running = False
                periodic_message.cancel()

bot.run(token, log_handler=handler, log_level=logging.DEBUG)