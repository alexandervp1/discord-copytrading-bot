import discord
from discord.ext import commands
import asyncio
from bot.charts import get_chart
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
SERVER_ID = int(os.getenv('SERVER_ID'))
CRYPTO1_ID = int(os.getenv('CRYPTO1_ID'))
CRYPTO1_CHANNEL_ID = {int(x) for x in os.environ["CRYPTO1_CHANNEL_ID"].split(",")}
CHANNEL_ID = {int(x) for x in os.getenv('CHANNEL_ID').split(',')}
GUILDS = [discord.Object(id=SERVER_ID), discord.Object(id=CRYPTO1_ID)]
LISTEN_CHANNELS = CHANNEL_ID | CRYPTO1_CHANNEL_ID

class Client(commands.Bot):
    #Events
    async def on_ready(self):
        print(f"Logged in as {self.user}.")

        for g in self.guilds:
            print(f'Server: {g.name}, {g.id}')
            
        for g in GUILDS:
            try:
              synced = await self.tree.sync(guild=g)
              print(f'Synced {len(synced)} commands to guild {g.id}')

            except Exception as e:
              print(f'Error syncing commands for {g.id} {e}')
    


    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id not in LISTEN_CHANNELS:
            return
        print(f"[{message.channel.name}] {message.author}: {message.content}")

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="/", intents=intents)

#Slash Commands
@client.tree.command(name="btc-chart", description="Bitcoin Chart"
" (Display all timeframes through buttons)", guilds=GUILDS)

async def btc_1d(interaction: discord.Interaction):
    await interaction.response.defer()
    buf = await asyncio.to_thread(get_chart, "BTC/USDT", "1d" )
    await interaction.followup.send(file=discord.File(buf, filename="btc-chart.png"))



client.run(token)