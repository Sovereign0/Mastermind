
import discord
from discord.ext import commands
from discord import app_commands

# Import game modules
from BEAUTYCON.beauty_contest import bot as beauty_bot, tree
from bloody.host_bd import register_host_bd
from bloody.code_bd import register_code_bd
from bloody.guess_bd import register_guess_bd
from bloody.resign_bd import register_resign_bd
from bloody.cancel_bd import register_cancel_bd
from bloody.list_bd import register_list_bd
# View BD command temporarily removed
from unravel.host_unravel import register_host_unravel
from unravel.code_unravel import register_code_unravel
from unravel.guess_unravel import register_guess_unravel
from unravel.resign import register_resign_unravel
from unravel.cancel_unravel import register_cancel_unravel
from unravel.list import register_list_command
from OTHERS.help import Help
from OTHERS.feedback import register_feedback_commands
from game import BloodyDotty
from utils import update_stats
from stats import register_stats_commands

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Game state storage
games = {}
player_games = {}
bloody_dotty = BloodyDotty()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()
    
async def setup():
    # Register all game commands
    await register_host_bd(bot, bloody_dotty, games, player_games)
    await register_code_bd(bot, bloody_dotty, games, player_games)
    await register_guess_bd(bot, bloody_dotty, games, player_games, None)
    await register_resign_bd(bot, games, player_games)
    await register_cancel_bd(bot, games, player_games)
    await register_list_bd(bot, games)
    
    # Register unravel commands
    await register_host_unravel(bot, games)
    await register_code_unravel(bot, games)
    await register_guess_unravel(bot, games)
    await register_resign_unravel(bot, games)
    await register_cancel_unravel(bot, games)
    await register_list_command(bot, games)
    
    # Register utility commands
    await register_feedback_commands(bot)
    await register_stats_commands(bot)
    await bot.add_cog(Help(bot))

bot.setup_hook = setup

# Run the bot
import os
TOKEN = os.environ['DISCORD_TOKEN']
bot.run(TOKEN)
