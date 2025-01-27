import discord
import random
from discord import app_commands

async def register_code_bd(bot, bloody_dotty, games, player_games):
    @bot.tree.command(name="code_bd", description="Submit your number for Bloody Dotty")
    async def code_bd(interaction: discord.Interaction, number: int):
        # Check if the user is in an active game
        if interaction.user.id not in player_games:
            await interaction.response.send_message("No active Bloody Dotty game. Start a new game first.", ephemeral=True)
            return

        # Get the current game for the player
        game_id = player_games[interaction.user.id]
        current_game = games.get(game_id)

        if number < 1 or number > 10:
            await interaction.response.send_message("Invalid number. Please enter a number between 1 and 10.", ephemeral=True)
            return

        if interaction.user.id == current_game.host.id:
            if current_game.host_number is not None:
                await interaction.response.send_message("You have already set your number. You cannot change it.", ephemeral=True)
                return
            current_game.host_number = number
            await interaction.response.send_message(f"Your number {number} has been set.", ephemeral=True)
        elif interaction.user.id == current_game.opponent.id:
            if current_game.opponent_number is not None:
                await interaction.response.send_message("You have already set your number. You cannot change it.", ephemeral=True)
                return
            current_game.opponent_number = number
            await interaction.response.send_message(f"Your number {number} has been set.", ephemeral=True)
        else:
            await interaction.response.send_message("You're not part of the ongoing game.", ephemeral=True)

        # If both players have set their numbers, the game can start
        if current_game.host_number is not None and current_game.opponent_number is not None:
            current_game.turn = random.choice([current_game.host, current_game.opponent])
            await current_game.channel.send(f'Both numbers are set! Let the game begin! It\'s {current_game.turn.mention}\'s turn to guess the sum.')
