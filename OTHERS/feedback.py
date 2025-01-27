import discord
from discord import app_commands
from discord.ext import commands 
import os
import json

FEEDBACK_DIR = 'feedbacks'
FEEDBACK_FILE = os.path.join(FEEDBACK_DIR, 'feedback.json')

async def save_feedback(user, suggestion):
    if not os.path.exists(FEEDBACK_DIR):
        os.makedirs(FEEDBACK_DIR)

    feedback_data = {}
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            feedback_data = json.load(f)

    feedback_data[user.id] = {
        "username": str(user),
        "suggestion": suggestion
    }

    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=4)

class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="feedback", description="Submit your suggestions")
    async def feedback(self, interaction: discord.Interaction, suggestion: str):
        await save_feedback(interaction.user, suggestion)
        await interaction.response.send_message("Thank you for your feedback!", ephemeral=False)

async def register_feedback_commands(bot):
    await bot.add_cog(Feedback(bot))

