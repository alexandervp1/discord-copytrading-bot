import discord
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ('DISCORD_TOKEN')
CHANNEL_IDS = {int(x) for x in os.environ('CHANNEL_IDS').split(',')}

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}.")

    async def on_message(self, message):
        if message.author == message.user:
            return
        if message.channel.id not in CHANNEL_IDS:
            return
        print(f'[{message.channel.name}] {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(token)